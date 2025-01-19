import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import requests
from flask import Response, g, request

from flask_inputfilter.Condition.BaseCondition import BaseCondition
from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Filter import BaseFilter
from flask_inputfilter.Model import ExternalApiConfig
from flask_inputfilter.Validator import BaseValidator


class InputFilter:
    """
    Base class for input filters.
    """

    def __init__(self, methods: Optional[List[str]] = None) -> None:
        self.methods = methods or ["GET", "POST", "PATCH", "PUT", "DELETE"]
        self.fields = {}
        self.conditions = []
        self.global_filters = []
        self.global_validators = []

    def add(
        self,
        name: str,
        required: bool = False,
        default: Any = None,
        fallback: Any = None,
        filters: Optional[List[BaseFilter]] = None,
        validators: Optional[List[BaseValidator]] = None,
        steps: Optional[List[Union[BaseFilter, BaseValidator]]] = None,
        external_api: Optional[ExternalApiConfig] = None,
    ) -> None:
        """
        Add the field to the input filter.

        :param name: The name of the field.
        :param required: Whether the field is required.
        :param default: The default value of the field.
        :param fallback: The fallback value of the field, if validations fails
        or field None, although it is required .
        :param filters: The filters to apply to the field value.
        :param validators: The validators to apply to the field value.
        :param steps: Allows to apply multiple filters and validators
        in a specific order.
        :param external_api: Configuration for an external API call.
        """

        self.fields[name] = {
            "required": required,
            "default": default,
            "fallback": fallback,
            "filters": filters or [],
            "validators": validators or [],
            "steps": steps or [],
            "external_api": external_api,
        }

    def addCondition(self, condition: BaseCondition) -> None:
        """
        Add a condition to the input filter.
        """
        self.conditions.append(condition)

    def addGlobalFilter(self, filter_: BaseFilter) -> None:
        """
        Add a global filter to be applied to all fields.
        """
        self.global_filters.append(filter_)

    def addGlobalValidator(self, validator: BaseValidator) -> None:
        """
        Add a global validator to be applied to all fields.
        """
        self.global_validators.append(validator)

    def __applyFilters(self, field_name: str, value: Any) -> Any:
        """
        Apply filters to the field value.
        """

        if value is None:
            return value

        for filter_ in self.global_filters:
            value = filter_.apply(value)

        field = self.fields.get(field_name)

        for filter_ in field.get("filters"):
            value = filter_.apply(value)

        return value

    def __validateField(
        self, field_name: str, field_info: Any, value: Any
    ) -> None:
        """
        Validate the field value.
        """

        if value is None:
            return

        try:
            for validator in self.global_validators:
                validator.validate(value)

            field = self.fields.get(field_name)

            for validator in field.get("validators"):
                validator.validate(value)
        except ValidationError:
            if field_info.get("fallback") is None:
                raise

            return field_info.get("fallback")

    def __applySteps(
        self, field_name: str, field_info: Any, value: Any
    ) -> Any:
        """
        Apply multiple filters and validators in a specific order.
        """

        if value is None:
            return

        field = self.fields.get(field_name)

        try:
            for step in field.get("steps"):
                if isinstance(step, BaseFilter):
                    value = step.apply(value)
                elif isinstance(step, BaseValidator):
                    step.validate(value)
        except ValidationError:
            if field_info.get("fallback") is None:
                raise
            return field_info.get("fallback")

        return value

    def __callExternalApi(
        self, field_info: Any, validated_data: dict
    ) -> Optional[Any]:
        """
        Führt den API-Aufruf durch und gibt den Wert zurück,
        der im Antwortkörper zu finden ist.
        """

        config: ExternalApiConfig = field_info.get("external_api")

        requestData = {
            "headers": {},
            "params": {},
        }

        if config.api_key:
            requestData["headers"]["Authorization"] = (
                f"Bearer " f"{config.api_key}"
            )

        if config.headers:
            requestData["headers"].update(config.headers)

        if config.params:
            requestData["params"] = self.__replacePlaceholdersInParams(
                config.params, validated_data
            )

        requestData["url"] = self.__replacePlaceholders(
            config.url, validated_data
        )
        requestData["method"] = config.method

        try:
            response = requests.request(**requestData)

            if response.status_code != 200:
                raise ValidationError(
                    f"External API call failed with "
                    f"status code {response.status_code}"
                )

            result = response.json()

            data_key = config.data_key
            if data_key:
                return result.get(data_key)

            return result
        except Exception:
            if field_info and field_info.get("fallback") is None:
                raise ValidationError(
                    f"External API call failed for field "
                    f"'{config.data_key}'."
                )

            return field_info.get("fallback")

    @staticmethod
    def __replacePlaceholders(value: str, validated_data: dict) -> str:
        """
        Replace all placeholders, marked with '{{ }}' in value
        with the corresponding values from validated_data.
        """

        return re.sub(
            r"{{(.*?)}}",
            lambda match: str(validated_data.get(match.group(1))),
            value,
        )

    def __replacePlaceholdersInParams(
        self, params: dict, validated_data: dict
    ) -> dict:
        """
        Replace all placeholders in params with the
        corresponding values from validated_data.
        """
        return {
            key: self.__replacePlaceholders(value, validated_data)
            if isinstance(value, str)
            else value
            for key, value in params.items()
        }

    @staticmethod
    def __checkForRequired(
        field_name: str, field_info: dict, value: Any
    ) -> Any:
        """
        Determine the value of the field, considering the required and
        fallback attributes.

        If the field is not required and no value is provided, the default
        value is returned.
        If the field is required and no value is provided, the fallback
        value is returned.
        If no of the above conditions are met, a ValidationError is raised.
        """

        if value is not None:
            return value

        if not field_info.get("required"):
            return field_info.get("default")

        if field_info.get("fallback") is not None:
            return field_info.get("fallback")

        raise ValidationError(f"Field '{field_name}' is required.")

    def __checkConditions(self, validated_data: dict) -> None:
        for condition in self.conditions:
            if not condition.check(validated_data):
                raise ValidationError(f"Condition '{condition}' not met.")

    def validateData(
        self, data: Dict[str, Any], kwargs: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Validate the input data, considering both request data and
        URL parameters (kwargs).
        """

        if kwargs is None:
            kwargs = {}

        validated_data = {}
        combined_data = {**data, **kwargs}

        for field_name, field_info in self.fields.items():
            value = combined_data.get(field_name)

            value = self.__applyFilters(field_name, value)

            value = (
                self.__validateField(field_name, field_info, value) or value
            )

            value = self.__applySteps(field_name, field_info, value) or value

            if field_info.get("external_api"):
                value = self.__callExternalApi(field_info, validated_data)

            value = self.__checkForRequired(field_name, field_info, value)

            validated_data[field_name] = value

        self.__checkConditions(validated_data)

        return validated_data

    @classmethod
    def validate(
        cls,
    ) -> Callable[
        [Any],
        Callable[
            [Tuple[Any, ...], Dict[str, Any]],
            Union[Response, Tuple[Any, Dict[str, Any]]],
        ],
    ]:
        """
        Decorator for validating input data in routes.
        """

        def decorator(
            f,
        ) -> Callable[
            [Tuple[Any, ...], Dict[str, Any]],
            Union[Response, Tuple[Any, Dict[str, Any]]],
        ]:
            def wrapper(
                *args, **kwargs
            ) -> Union[Response, Tuple[Any, Dict[str, Any]]]:
                if request.method not in cls().methods:
                    return Response(status=405, response="Method Not Allowed")

                data = request.json if request.is_json else request.args

                try:
                    g.validated_data = cls().validateData(data, kwargs)

                except ValidationError as e:
                    return Response(status=400, response=str(e))

                return f(*args, **kwargs)

            return wrapper

        return decorator

import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import requests
from flask import Response, g, request
from typing_extensions import final

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

    @final
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
        copy: Optional[str] = None,
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
        :param copy: The name of the field to copy the value from.
        """

        self.fields[name] = {
            "required": required,
            "default": default,
            "fallback": fallback,
            "filters": filters or [],
            "validators": validators or [],
            "steps": steps or [],
            "external_api": external_api,
            "copy": copy,
        }

    @final
    def addCondition(self, condition: BaseCondition) -> None:
        """
        Add a condition to the input filter.
        """
        self.conditions.append(condition)

    @final
    def addGlobalFilter(self, filter_: BaseFilter) -> None:
        """
        Add a global filter to be applied to all fields.
        """
        self.global_filters.append(filter_)

    @final
    def addGlobalValidator(self, validator: BaseValidator) -> None:
        """
        Add a global validator to be applied to all fields.
        """
        self.global_validators.append(validator)

    @final
    def __applyFilters(self, filters: List[BaseFilter], value: Any) -> Any:
        """
        Apply filters to the field value.
        """

        if value is None:
            return value

        for filter_ in self.global_filters + filters:
            value = filter_.apply(value)

        return value

    @final
    def __validateField(
        self, validators: List[BaseValidator], fallback: Any, value: Any
    ) -> None:
        """
        Validate the field value.
        """

        if value is None:
            return

        try:
            for validator in self.global_validators + validators:
                validator.validate(value)
        except ValidationError:
            if fallback is None:
                raise

            return fallback

    @final
    def __applySteps(
        self,
        steps: List[Union[BaseFilter, BaseValidator]],
        fallback: Any,
        value: Any,
    ) -> Any:
        """
        Apply multiple filters and validators in a specific order.
        """

        if value is None:
            return

        try:
            for step in steps:
                if isinstance(step, BaseFilter):
                    value = step.apply(value)
                elif isinstance(step, BaseValidator):
                    step.validate(value)
        except ValidationError:
            if fallback is None:
                raise
            return fallback

        return value

    @final
    def __callExternalApi(
        self, config: ExternalApiConfig, fallback: Any, validated_data: dict
    ) -> Optional[Any]:
        """
        Führt den API-Aufruf durch und gibt den Wert zurück,
        der im Antwortkörper zu finden ist.
        """

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
            if fallback is None:
                raise ValidationError(
                    f"External API call failed for field "
                    f"'{config.data_key}'."
                )

            return fallback

    @staticmethod
    @final
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

    @final
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
    @final
    def __checkForRequired(
        field_name: str,
        required: bool,
        default: Any,
        fallback: Any,
        value: Any,
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

        if not required:
            return default

        if fallback is not None:
            return fallback

        raise ValidationError(f"Field '{field_name}' is required.")

    def __checkConditions(self, validated_data: dict) -> None:
        for condition in self.conditions:
            if not condition.check(validated_data):
                raise ValidationError(f"Condition '{condition}' not met.")

    @final
    def validateData(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the input data, considering both request data and
        URL parameters (kwargs).
        """

        validated_data = {}

        for field_name, field_info in self.fields.items():
            value = data.get(field_name)

            required = field_info["required"]
            default = field_info["default"]
            fallback = field_info["fallback"]
            filters = field_info["filters"]
            validators = field_info["validators"]
            steps = field_info["steps"]
            external_api = field_info["external_api"]
            copy = field_info["copy"]

            if copy:
                value = validated_data.get(copy)

            if external_api:
                value = self.__callExternalApi(
                    external_api, fallback, validated_data
                )

            value = self.__applyFilters(filters, value)

            value = self.__validateField(validators, fallback, value) or value

            value = self.__applySteps(steps, fallback, value) or value

            value = self.__checkForRequired(
                field_name, required, default, fallback, value
            )

            validated_data[field_name] = value

        self.__checkConditions(validated_data)

        return validated_data

    @classmethod
    @final
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
                input_filter = cls()
                if request.method not in input_filter.methods:
                    return Response(status=405, response="Method Not Allowed")

                data = request.json if request.is_json else request.args

                try:
                    g.validated_data = input_filter.validateData(data)

                except ValidationError as e:
                    return Response(status=400, response=str(e))

                return f(*args, **kwargs)

            return wrapper

        return decorator

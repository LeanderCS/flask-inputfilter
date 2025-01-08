import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import requests
from flask import Response, g, request
from typing_extensions import TypedDict

from .Exception import ValidationError
from .Filter.BaseFilter import BaseFilter
from .Validator.BaseValidator import BaseValidator


class ExternalApiConfig(TypedDict):
    """
    Configuration for an external API call.

    :param url: The URL of the external API.
    :param method: The HTTP method to use.
    :param params: The parameters to send to the API.
    :param data_key: The key in the response JSON to use
    """

    url: str
    method: str
    params: Optional[Dict[str, str]]
    data_key: Optional[str]
    api_key: Optional[str]


class InputFilter:
    """
    Base class for input filters.
    """

    def __init__(self) -> None:

        self.fields = {}

    def add(
        self,
        name: str,
        required: bool = False,
        default: Any = None,
        fallback: Any = None,
        filters: Optional[List[BaseFilter]] = None,
        validators: Optional[List[BaseValidator]] = None,
        external_api: Optional[Dict[str, Union[str, Dict[str, str]]]] = None,
    ) -> None:
        """
        Add the field to the input filter.

        :param name: The name of the field.
        :param required: Whether the field is required.
        :param default: The default value of the field.
        :param fallback: The fallback value of the field.
        :param filters: The filters to apply to the field value.
        :param validators: The validators to apply to the field value.
        :param external_api: Configuration for an external API call.
        """

        self.fields[name] = {
            "required": required,
            "default": default,
            "fallback": fallback,
            "filters": filters or [],
            "validators": validators or [],
            "external_api": external_api,
        }

    def _applyFilters(self, field_name: str, value: Any) -> Any:
        """
        Apply filters to the field value.
        """

        field = self.fields.get(field_name)

        if not field:
            return value

        for filter_ in field["filters"]:
            value = filter_.apply(value)

        return value

    def _validateField(self, field_name: str, value: Any) -> None:
        """
        Validate the field value.
        """

        field = self.fields.get(field_name)

        if not field:
            return

        for validator in field["validators"]:
            validator.validate(value)

    def _callExternalApi(
        self, config: dict, validated_data: dict
    ) -> Optional[Any]:
        """
        Führt den API-Aufruf durch und gibt den Wert zurück,
        der im Antwortkörper zu finden ist.
        """

        requestData = {}

        if "api_key" in config:
            requestData["headers"][
                "Authorization"
            ] = f"Bearer {config['api_key']}"

        if "headers" in config:
            requestData["headers"].update(config["headers"])

        if "params" in config:
            requestData["params"] = self.__replacePlaceholdersInParams(
                config["params"], validated_data
            )

        requestData["url"] = self.__replacePlaceholders(
            config["url"], validated_data
        )
        requestData["method"] = config["method"]

        response = requests.request(**requestData)

        if response.status_code != 200:
            raise ValidationError(
                f"External API call failed with status code {response.status_code}"
            )

        result = response.json()

        data_key = config.get("data_key", None)
        if data_key:
            return result.get(data_key)

        return result

    @staticmethod
    def __replacePlaceholders(url: str, validated_data: dict) -> str:
        """
        Ersetzt alle Platzhalter in der URL, die mit {{}} definiert sind,
        durch die entsprechenden Werte aus den Parametern.
        """

        return re.sub(
            r"{{(.*?)}}",
            lambda match: str(validated_data.get(match.group(1))),
            url,
        )

    @staticmethod
    def __replacePlaceholdersInParams(
        params: dict, validated_data: dict
    ) -> dict:
        """
        Replace all placeholders in params with the
        corresponding values from validated_data.
        """
        replaced_params = {}
        for key, value in params.items():
            if isinstance(value, str):
                replaced_value = re.sub(
                    r"{{(.*?)}}",
                    lambda match: str(validated_data.get(match.group(1), "")),
                    value,
                )
                replaced_params[key] = replaced_value
            else:
                replaced_params[key] = value
        return replaced_params

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

            # Apply filters
            value = self._applyFilters(field_name, value)

            # Check for required field
            if value is None:
                if (
                    field_info["required"]
                    and field_info["external_api"] is None
                ):
                    if field_info["fallback"] is None:
                        raise ValidationError(
                            f"Field '{field_name}' is required."
                        )

                    value = field_info["fallback"]

                if field_info["default"] is not None:
                    value = field_info["default"]

            # Validate field
            if value is not None:
                try:
                    self._validateField(field_name, value)
                except ValidationError:
                    if field_info["fallback"] is not None:
                        value = field_info["fallback"]
                    else:
                        raise

            # External API call
            if field_info["external_api"]:
                external_api_config = field_info["external_api"]

                try:
                    value = self._callExternalApi(
                        external_api_config, validated_data
                    )

                except ValidationError as e:
                    if field_info["fallback"] is None:
                        print(e)
                        raise ValidationError(
                            f"External API call failed for field '{field_name}'."
                        )

                    value = field_info["fallback"]

                if value is None:
                    if field_info["required"]:
                        if field_info["fallback"] is None:
                            raise ValidationError(
                                f"Field '{field_name}' is required."
                            )

                        value = field_info["fallback"]

                    if field_info["default"] is not None:
                        value = field_info["default"]

            validated_data[field_name] = value

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
                if request.method == "GET":
                    data = request.args

                elif request.method in ["POST", "PUT", "DELETE"]:
                    if not request.is_json:
                        data = request.args

                    else:
                        data = request.json

                else:
                    return Response(
                        status=415, response="Unsupported method Type"
                    )

                inputFilter = cls()

                try:
                    g.validated_data = inputFilter.validateData(data, kwargs)

                except ValidationError as e:
                    return Response(status=400, response=str(e))

                return f(*args, **kwargs)

            return wrapper

        return decorator

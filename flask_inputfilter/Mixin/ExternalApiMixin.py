import re
from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Mixin import BaseMixin
from flask_inputfilter.Model import ExternalApiConfig

API_PLACEHOLDER_PATTERN = re.compile(r"{{(.*?)}}")


class ExternalApiMixin(BaseMixin):
    def __callExternalApi(
        self, config: ExternalApiConfig, fallback: Any, validated_data: dict
    ) -> Optional[Any]:
        """
        Makes a call to an external API using provided configuration and
        returns the response.

        Summary:
        The function constructs a request based on the given API
        configuration and validated data, including headers, parameters,
        and other request settings. It utilizes the `requests` library
        to send the API call and processes the response. If a fallback
        value is supplied, it is returned in case of any failure during
        the API call. If no fallback is provided, a validation error is
        raised.

        Parameters:
            config:
                An object containing the configuration details for the
                external API call, such as URL, headers, method, and API key.
            fallback:
                The value to be returned in case the external API call fails.
            validated_data:
                The dictionary containing data used to replace placeholders
                in the URL and parameters of the API request.

        Returns:
            Optional[Any]:
                The JSON-decoded response from the API, or the fallback
                value if the call fails and a fallback is provided.

        Raises:
            ValidationError
                Raised if the external API call does not succeed and no
                fallback value is provided.
        """
        import logging

        import requests

        logger = logging.getLogger(__name__)

        data_key = config.data_key

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
                logger.error(
                    f"External_api request inside of InputFilter "
                    f"failed: {response.text}"
                )
                raise

            result = response.json()

            if data_key:
                return result.get(data_key)

            return result
        except Exception:
            if fallback is None:
                raise ValidationError(
                    f"External API call failed for field " f"'{data_key}'."
                )

            return fallback

    @staticmethod
    def __replacePlaceholders(value: str, validated_data: dict) -> str:
        """
        Replace all placeholders, marked with '{{ }}' in value
        with the corresponding values from validated_data.
        """
        return API_PLACEHOLDER_PATTERN.sub(
            lambda match: str(validated_data.get(match.group(1))),
            value,
        )

    def __replacePlaceholdersInParams(
        self, params: dict, validated_data: dict
    ) -> dict:
        """
        Replace all placeholders in params with the corresponding
        values from validated_data.
        """
        return {
            key: self.__replacePlaceholders(value, validated_data)
            if isinstance(value, str)
            else value
            for key, value in params.items()
        }

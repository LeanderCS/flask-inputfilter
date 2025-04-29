from __future__ import annotations

import re
from typing import Any, Dict, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import ExternalApiConfig


class ExternalApiMixin:
    @staticmethod
    def call_external_api(
        config: ExternalApiConfig,
        fallback: Any,
        validated_data: Dict[str, Any],
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
            config (ExternalApiConfig):
                An object containing the configuration details for the
                external API call, such as URL, headers, method, and API key.
            fallback (Any):
                The value to be returned in case the external API call fails.
            validated_data (Dict[str, Any]):
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

        request_data = {
            "headers": {},
            "params": {},
        }

        if config.api_key:
            request_data["headers"][
                "Authorization"
            ] = f"Bearer {config.api_key}"

        if config.headers:
            request_data["headers"].update(config.headers)

        if config.params:
            request_data[
                "params"
            ] = ExternalApiMixin.replace_placeholders_in_params(
                config.params, validated_data
            )

        request_data["url"] = ExternalApiMixin.replace_placeholders(
            config.url, validated_data
        )
        request_data["method"] = config.method

        try:
            response = requests.request(**request_data)
            result = response.json()
        except requests.exceptions.RequestException:
            if fallback is None:
                logger.exception("External API request failed unexpectedly.")
                raise ValidationError(
                    f"External API call failed for field'{data_key}'."
                )
            return fallback
        except ValueError:
            if fallback is None:
                logger.exception(
                    "External API response could not be parsed to json."
                )
                raise ValidationError(
                    f"External API call failed for field '{data_key}'."
                )
            return fallback

        if response.status_code != 200:
            if fallback is None:
                logger.error(
                    f"External API request failed with status "
                    f"{response.status_code}: {response.text}"
                )
                raise ValidationError(
                    f"External API call failed for field '{data_key}'."
                )
            return fallback

        return result.get(data_key) if data_key else result

    @staticmethod
    def replace_placeholders(
        value: str, validated_data: Dict[str, Any]
    ) -> str:
        """
        Replace all placeholders, marked with '{{ }}' in value with the
        corresponding values from validated_data.

        Params:
            value (str): The string containing placeholders to be replaced.
            validated_data (Dict[str, Any]): The dictionary containing
                the values to replace the placeholders with.

        Returns:
            str: The value with all placeholders replaced with
                 the corresponding values from validated_data.
        """
        return re.compile(r"{{(.*?)}}").sub(
            lambda match: str(validated_data.get(match.group(1))),
            value,
        )

    @staticmethod
    def replace_placeholders_in_params(
        params: dict, validated_data: Dict[str, Any]
    ) -> dict:
        """
        Replace all placeholders in params with the corresponding values from
        validated_data.

        Params:
            params (dict): The params dictionary containing placeholders.
            validated_data (Dict[str, Any]): The dictionary containing
                the values to replace the placeholders with.

        Returns:
            dict: The params dictionary with all placeholders replaced
                  with the corresponding values from validated_data.
        """
        return {
            key: ExternalApiMixin.replace_placeholders(value, validated_data)
            if isinstance(value, str)
            else value
            for key, value in params.items()
        }

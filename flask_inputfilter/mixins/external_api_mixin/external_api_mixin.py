from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Optional

from flask_inputfilter.exceptions import ValidationError

if TYPE_CHECKING:
    from flask_inputfilter.models import ExternalApiConfig


class ExternalApiMixin:
    __slots__ = ()

    @staticmethod
    def call_external_api(
        config: ExternalApiConfig,
        fallback: Any,
        validated_data: dict[str, Any],
    ) -> Optional[Any]:
        """
        The function constructs a request based on the given API configuration
        and validated data, including headers, parameters, and other request
        settings. It utilizes the `requests` library to send the API call and
        processes the response. If a fallback value is supplied, it is returned
        in case of any failure during the API call. If no fallback is provided,
        a validation error is raised.

        **Parameters:**

        - **config** (*ExternalApiConfig*):
          An object containing the configuration details for the
          external API call, such as URL, headers, method, and API key.
        - **fallback** (*Any*):
          The value to be returned in case the external API call fails.
        - **validated_data** (*dict[str, Any]*):
          The dictionary containing data used to replace placeholders
          in the URL and parameters of the API request.

        **Returns:**

        - (*Optional[Any]*):
          The JSON-decoded response from the API, or the fallback
          value if the call fails and a fallback is provided.

        **Raises:**

        - **ValidationError**:
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
            request_data["headers"]["Authorization"] = (
                f"Bearer {config.api_key}"
            )

        if config.headers:
            request_data["headers"].update(config.headers)

        if config.params:
            request_data["params"] = (
                ExternalApiMixin.replace_placeholders_in_params(
                    config.params, validated_data
                )
            )

        request_data["url"] = ExternalApiMixin.replace_placeholders(
            config.url, validated_data
        )
        request_data["method"] = config.method

        try:
            response = requests.request(timeout=30, **request_data)
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
        value: str,
        validated_data: dict[str, Any],
    ) -> str:
        """
        Replace all placeholders, marked with '{{ }}' in value with the
        corresponding values from validated_data.

        **Parameters:**

        - **value** (**str**): The string containing placeholders to
          be replaced.
        - **validated_data** (**dict[str, Any]**): The dictionary containing
          the values to replace the placeholders with.

        **Returns:**

        - (*str*): The value with all placeholders replaced with
          the corresponding values from validated_data.
        """
        return re.compile(r"{{(.*?)}}").sub(
            lambda match: str(validated_data.get(match.group(1))),
            value,
        )

    @staticmethod
    def replace_placeholders_in_params(
        params: dict,
        validated_data: dict[str, Any],
    ) -> dict:
        """
        Replace all placeholders in params with the corresponding values from
        validated_data.

        **Parameters:**

        - **params** (*dict*): The params dictionary containing placeholders.
        - **validated_data** (*dict[str, Any]*): The dictionary containing
          the values to replace the placeholders with.

        **Returns:**

        - (*dict*): The params dictionary with all placeholders replaced
          with the corresponding values from validated_data.
        """
        return {
            key: ExternalApiMixin.replace_placeholders(value, validated_data)
            if isinstance(value, str)
            else value
            for key, value in params.items()
        }

    @staticmethod
    async def call_external_api_async(
        config: ExternalApiConfig,
        fallback: Any,
        validated_data: dict[str, Any],
    ) -> Optional[Any]:
        """
        Async version of call_external_api using httpx.

        This function constructs an HTTP request based on the given API
        configuration and validated data. It uses the `httpx` library for
        async HTTP requests and includes retry logic for failed requests.

        **Parameters:**

        - **config** (*ExternalApiConfig*):
          Configuration for the external API call including URL, headers,
          method, timeout, and retry settings.
        - **fallback** (*Any*):
          The value to be returned in case the external API call fails.
        - **validated_data** (*dict[str, Any]*):
          The dictionary containing data used to replace placeholders
          in the URL and parameters of the API request.

        **Returns:**

        - (*Optional[Any]*):
          The JSON-decoded response from the API, or the fallback
          value if the call fails and a fallback is provided.

        **Raises:**

        - **ValidationError**:
          Raised if the external API call does not succeed and no
          fallback value is provided.
        - **ImportError**:
          Raised if httpx is not installed.
        """
        import asyncio
        import logging

        try:
            import httpx
        except ImportError as e:
            raise ImportError(
                "httpx is required for async external API calls. "
                "Install with: pip install flask-inputfilter[async]"
            ) from e

        logger = logging.getLogger(__name__)
        data_key = config.data_key

        # Build request data
        request_data = {
            "headers": {},
            "params": {},
        }

        if config.api_key:
            request_data["headers"]["Authorization"] = (
                f"Bearer {config.api_key}"
            )

        if config.headers:
            request_data["headers"].update(config.headers)

        if config.params:
            request_data["params"] = (
                ExternalApiMixin.replace_placeholders_in_params(
                    config.params, validated_data
                )
            )

        request_data["url"] = ExternalApiMixin.replace_placeholders(
            config.url, validated_data
        )
        request_data["method"] = config.method

        # Retry logic
        for attempt in range(config.retry_count + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=config.timeout
                ) as client:
                    response = await client.request(**request_data)
                    result = response.json()

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

            except httpx.RequestError:
                if attempt < config.retry_count:
                    logger.warning(
                        f"External API request failed (attempt {attempt + 1}/"
                        f"{config.retry_count + 1}), retrying in "
                        f"{config.retry_delay}s..."
                    )
                    await asyncio.sleep(config.retry_delay)
                    continue

                if fallback is None:
                    logger.exception("External API request failed unexpectedly.")
                    raise ValidationError(
                        f"External API call failed for field '{data_key}'."
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

        # Should never reach here, but just in case
        return fallback

    @staticmethod
    async def call_external_apis_parallel(
        configs_and_fallbacks: list[tuple[ExternalApiConfig, Any]],
        validated_data: dict[str, Any],
    ) -> list[Optional[Any]]:
        """
        Call multiple external APIs in parallel using asyncio.gather.

        This method enables concurrent execution of multiple external API
        calls, significantly reducing total request time when multiple
        fields require external API validation.

        **Parameters:**

        - **configs_and_fallbacks** (*list[tuple[ExternalApiConfig, Any]]*):
          List of tuples containing (config, fallback) pairs for each
          external API call to make.
        - **validated_data** (*dict[str, Any]*):
          The dictionary containing data used for placeholder replacement
          in all API requests.

        **Returns:**

        - (*list[Optional[Any]]*):
          List of results in the same order as the input configs.
          Each result is either the API response or the fallback value.

        **Example:**

        .. code-block:: python

            configs_and_fallbacks = [
                (user_api_config, None),
                (company_api_config, {}),
                (product_api_config, None),
            ]

            # All 3 API calls execute in parallel
            results = await call_external_apis_parallel(
                configs_and_fallbacks,
                validated_data
            )
        """
        import asyncio

        tasks = [
            ExternalApiMixin.call_external_api_async(
                config, fallback, validated_data
            )
            for config, fallback in configs_and_fallbacks
        ]

        return await asyncio.gather(*tasks)

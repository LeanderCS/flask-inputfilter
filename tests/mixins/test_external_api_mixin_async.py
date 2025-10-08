import unittest
from unittest.mock import AsyncMock, Mock, patch

import pytest

from flask_inputfilter.mixins import ExternalApiMixin
from flask_inputfilter.models import ExternalApiConfig
from flask_inputfilter.exceptions import ValidationError


class TestExternalApiMixinAsync(unittest.IsolatedAsyncioTestCase):
    """Test suite for async external API mixin functionality."""

    async def test_call_external_api_async_basic(self):
        """Test basic async external API call."""
        config = ExternalApiConfig(
            url="https://api.example.com/users/123",
            method="GET",
            data_key="user",
            async_mode=True
        )

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"user": {"id": 123, "name": "Test"}}

        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            mock_client.return_value = mock_context

            result = await ExternalApiMixin.call_external_api_async(
                config,
                fallback=None,
                validated_data={}
            )

            self.assertEqual(result, {"id": 123, "name": "Test"})

    async def test_call_external_api_async_with_fallback(self):
        """Test async API call with fallback on failure."""
        config = ExternalApiConfig(
            url="https://api.example.com/users/123",
            method="GET",
            data_key="user",
            async_mode=True
        )

        fallback_value = {"id": 0, "name": "Unknown"}

        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.request = AsyncMock(
                side_effect=Exception("Network error")
            )
            mock_client.return_value = mock_context

            result = await ExternalApiMixin.call_external_api_async(
                config,
                fallback=fallback_value,
                validated_data={}
            )

            self.assertEqual(result, fallback_value)

    async def test_call_external_api_async_retry_logic(self):
        """Test retry logic on failed requests."""
        config = ExternalApiConfig(
            url="https://api.example.com/users/123",
            method="GET",
            data_key="user",
            async_mode=True,
            retry_count=2,
            retry_delay=0.1  # Short delay for tests
        )

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"user": {"id": 123}}

        call_count = 0

        async def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                # First call fails
                raise Exception("Temporary error")
            # Second call succeeds
            return mock_response

        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.request = mock_request
            mock_client.return_value = mock_context

            result = await ExternalApiMixin.call_external_api_async(
                config,
                fallback=None,
                validated_data={}
            )

            self.assertEqual(result, {"id": 123})
            self.assertEqual(call_count, 2)  # Failed once, succeeded on retry

    async def test_call_external_api_async_no_httpx(self):
        """Test that ImportError is raised when httpx is not installed."""
        config = ExternalApiConfig(
            url="https://api.example.com/users/123",
            method="GET",
            async_mode=True
        )

        with patch('builtins.__import__', side_effect=ImportError):
            with self.assertRaises(ImportError) as context:
                await ExternalApiMixin.call_external_api_async(
                    config,
                    fallback=None,
                    validated_data={}
                )

            self.assertIn("httpx is required", str(context.exception))

    async def test_call_external_apis_parallel(self):
        """Test parallel execution of multiple API calls."""
        config1 = ExternalApiConfig(
            url="https://api.example.com/users/1",
            method="GET",
            data_key="user",
            async_mode=True
        )

        config2 = ExternalApiConfig(
            url="https://api.example.com/products/1",
            method="GET",
            data_key="product",
            async_mode=True
        )

        config3 = ExternalApiConfig(
            url="https://api.example.com/orders/1",
            method="GET",
            data_key="order",
            async_mode=True
        )

        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {"user": {"id": 1}}

        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {"product": {"id": 1}}

        mock_response3 = Mock()
        mock_response3.status_code = 200
        mock_response3.json.return_value = {"order": {"id": 1}}

        responses = [mock_response1, mock_response2, mock_response3]
        call_index = 0

        async def mock_request(*args, **kwargs):
            nonlocal call_index
            response = responses[call_index]
            call_index += 1
            return response

        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.request = mock_request
            mock_client.return_value = mock_context

            configs_and_fallbacks = [
                (config1, None),
                (config2, None),
                (config3, None),
            ]

            results = await ExternalApiMixin.call_external_apis_parallel(
                configs_and_fallbacks,
                validated_data={}
            )

            self.assertEqual(len(results), 3)
            self.assertEqual(results[0], {"id": 1})
            self.assertEqual(results[1], {"id": 1})
            self.assertEqual(results[2], {"id": 1})

    async def test_call_external_api_async_timeout(self):
        """Test timeout configuration."""
        config = ExternalApiConfig(
            url="https://api.example.com/users/123",
            method="GET",
            async_mode=True,
            timeout=5
        )

        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_client.return_value = mock_context

            await ExternalApiMixin.call_external_api_async(
                config,
                fallback={"timeout": "test"},
                validated_data={}
            )

            # Verify timeout was passed to AsyncClient
            mock_client.assert_called_once_with(timeout=5)

    async def test_call_external_api_async_placeholder_replacement(self):
        """Test placeholder replacement in async API calls."""
        config = ExternalApiConfig(
            url="https://api.example.com/users/{{user_id}}",
            method="GET",
            data_key="user",
            async_mode=True
        )

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"user": {"id": 456}}

        captured_url = None

        async def mock_request(*args, **kwargs):
            nonlocal captured_url
            captured_url = kwargs.get('url')
            return mock_response

        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.request = mock_request
            mock_client.return_value = mock_context

            result = await ExternalApiMixin.call_external_api_async(
                config,
                fallback=None,
                validated_data={"user_id": "456"}
            )

            self.assertEqual(result, {"id": 456})
            self.assertEqual(captured_url, "https://api.example.com/users/456")

    async def test_call_external_api_async_non_200_status(self):
        """Test handling of non-200 status codes."""
        config = ExternalApiConfig(
            url="https://api.example.com/users/123",
            method="GET",
            async_mode=True
        )

        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.request = AsyncMock(
                return_value=mock_response
            )
            mock_client.return_value = mock_context

            with self.assertRaises(ValidationError):
                await ExternalApiMixin.call_external_api_async(
                    config,
                    fallback=None,
                    validated_data={}
                )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

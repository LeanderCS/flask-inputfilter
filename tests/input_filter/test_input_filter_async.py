import unittest
from unittest.mock import AsyncMock, Mock, patch

import pytest
from flask import Flask, g

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.models import ExternalApiConfig


class TestInputFilterAsync(unittest.IsolatedAsyncioTestCase):
    """Test suite for async InputFilter functionality."""

    async def test_async_decorator_auto_detection(self):
        """Test that @validate() automatically detects async routes."""

        class UserFilter(InputFilter):
            user_id: int = field(required=True)

        app = Flask(__name__)
        app.config['TESTING'] = True

        @app.route('/users', methods=['POST'])
        @UserFilter.validate()
        async def create_user():
            # This is an async route - decorator should detect it
            return {"data": g.validated_data}

        with app.test_client() as client:
            response = client.post(
                '/users',
                json={'user_id': 123}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['data']['user_id'], 123)

    async def test_async_external_api_parallel_execution(self):
        """Test that multiple async external APIs execute in parallel."""

        class OrderFilter(InputFilter):
            user_id: int = field(
                required=True,
                external_api=ExternalApiConfig(
                    url="https://api.example.com/users/{{user_id}}",
                    method="GET",
                    data_key="user",
                    async_mode=True
                )
            )

            product_id: int = field(
                required=True,
                external_api=ExternalApiConfig(
                    url="https://api.example.com/products/{{product_id}}",
                    method="GET",
                    data_key="product",
                    async_mode=True
                )
            )

        app = Flask(__name__)
        app.config['TESTING'] = True

        mock_user_response = Mock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {"user": {"id": 1, "name": "User1"}}

        mock_product_response = Mock()
        mock_product_response.status_code = 200
        mock_product_response.json.return_value = {"product": {"id": 2, "name": "Product1"}}

        responses = [mock_user_response, mock_product_response]
        call_index = 0

        async def mock_request(*args, **kwargs):
            nonlocal call_index
            response = responses[call_index]
            call_index += 1
            return response

        @app.route('/orders', methods=['POST'])
        @OrderFilter.validate()
        async def create_order():
            return {"data": g.validated_data}

        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.request = mock_request
            mock_client.return_value = mock_context

            with app.test_client() as client:
                response = client.post(
                    '/orders',
                    json={'user_id': 1, 'product_id': 2}
                )

                self.assertEqual(response.status_code, 200)
                # Both APIs should have been called
                self.assertEqual(call_index, 2)

    async def test_async_with_fallback(self):
        """Test async external API with fallback value."""

        class UserFilter(InputFilter):
            user_id: int = field(
                required=True,
                fallback={"id": 0, "name": "Unknown"},
                external_api=ExternalApiConfig(
                    url="https://api.example.com/users/{{user_id}}",
                    method="GET",
                    data_key="user",
                    async_mode=True
                )
            )

        app = Flask(__name__)
        app.config['TESTING'] = True

        @app.route('/users', methods=['POST'])
        @UserFilter.validate()
        async def get_user():
            return {"data": g.validated_data}

        # Mock a failed API call
        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.request = AsyncMock(
                side_effect=Exception("API Down")
            )
            mock_client.return_value = mock_context

            with app.test_client() as client:
                response = client.post(
                    '/users',
                    json={'user_id': 123}
                )

                self.assertEqual(response.status_code, 200)
                # Should use fallback
                self.assertEqual(response.json['data']['user_id'], {"id": 0, "name": "Unknown"})

    async def test_mixed_sync_async_external_apis(self):
        """Test InputFilter with mixed sync and async external APIs."""

        class MixedFilter(InputFilter):
            # Sync external API
            legacy_id: int = field(
                required=True,
                external_api=ExternalApiConfig(
                    url="https://legacy.example.com/data/{{legacy_id}}",
                    method="GET",
                    data_key="legacy",
                    async_mode=False  # Sync
                )
            )

            # Async external API
            modern_id: int = field(
                required=True,
                external_api=ExternalApiConfig(
                    url="https://modern.example.com/data/{{modern_id}}",
                    method="GET",
                    data_key="modern",
                    async_mode=True  # Async
                )
            )

        app = Flask(__name__)
        app.config['TESTING'] = True

        @app.route('/data', methods=['POST'])
        @MixedFilter.validate()
        async def get_data():
            return {"data": g.validated_data}

        # Mock both sync and async calls
        mock_sync_response = Mock()
        mock_sync_response.status_code = 200
        mock_sync_response.json.return_value = {"legacy": {"value": "old"}}

        mock_async_response = Mock()
        mock_async_response.status_code = 200
        mock_async_response.json.return_value = {"modern": {"value": "new"}}

        with patch('requests.request', return_value=mock_sync_response):
            with patch('httpx.AsyncClient') as mock_async_client:
                mock_context = AsyncMock()
                mock_context.__aenter__.return_value.request = AsyncMock(
                    return_value=mock_async_response
                )
                mock_async_client.return_value = mock_context

                with app.test_client() as client:
                    response = client.post(
                        '/data',
                        json={'legacy_id': 1, 'modern_id': 2}
                    )

                    self.assertEqual(response.status_code, 200)

    async def test_async_route_without_async_apis(self):
        """Test that async routes work even without async external APIs."""

        class SimpleFilter(InputFilter):
            name: str = field(required=True)

        app = Flask(__name__)
        app.config['TESTING'] = True

        @app.route('/simple', methods=['POST'])
        @SimpleFilter.validate()
        async def simple_route():
            # Async route, but no async external APIs
            # Should fall back to sync validation
            return {"data": g.validated_data}

        with app.test_client() as client:
            response = client.post(
                '/simple',
                json={'name': 'test'}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['data']['name'], 'test')

    async def test_async_with_retry_logic(self):
        """Test async external API with retry logic."""

        class UserFilter(InputFilter):
            user_id: int = field(
                required=True,
                external_api=ExternalApiConfig(
                    url="https://api.example.com/users/{{user_id}}",
                    method="GET",
                    data_key="user",
                    async_mode=True,
                    retry_count=2,
                    retry_delay=0.1
                )
            )

        app = Flask(__name__)
        app.config['TESTING'] = True

        call_count = 0

        async def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First call fails
                raise Exception("Temporary error")
            # Second call succeeds
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"user": {"id": 123}}
            return mock_response

        @app.route('/users', methods=['POST'])
        @UserFilter.validate()
        async def get_user():
            return {"data": g.validated_data, "attempts": call_count}

        with patch('httpx.AsyncClient') as mock_client:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.request = mock_request
            mock_client.return_value = mock_context

            with app.test_client() as client:
                response = client.post(
                    '/users',
                    json={'user_id': 123}
                )

                self.assertEqual(response.status_code, 200)
                # Should have retried once
                self.assertEqual(response.json['attempts'], 2)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

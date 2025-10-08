External API
============

This documentation provides a comprehensive overview of the external API functionality available in the `InputFilter` class.
It covers the configuration, core methods, and examples of usage for interacting with external APIs.

Overview
--------

The ``InputFilter`` class includes a mechanism for fetching data from external APIs during the input validation process.
This feature allows dynamic data retrieval based on user inputs, such as validating fields or fetching related data from an external service.

.. note::

    The external API functionality runs **before** all filters and validators have been executed.
    This means the data fetched from the external API can be validated and/or filtered as normal.

Configuration
-------------

The external API functionality is configured via the ``external_api`` parameter in the ``field`` function. This parameter accepts a dictionary with the following structure:

Fields of `ExternalApiConfig`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: External API Configuration Fields
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``url``
     - ``str``
     - The URL of the external API, with optional placeholders in ``{{ }}`` format.
   * - ``method``
     - ``str``
     - The HTTP method to use (e.g., ``GET``, ``POST``).
   * - ``params``
     - ``Optional[dict[str, str]]``
     - Query parameters for the API, with placeholders allowed.
   * - ``data_key``
     - ``Optional[str]``
     - Key in the JSON response to extract the required data.
   * - ``api_key``
     - ``Optional[str]``
     - API key for authorization, sent in the ``Authorization`` header.
   * - ``async_mode``
     - ``bool``
     - Enable async HTTP client (httpx) for parallel requests. Default: ``False``.
   * - ``timeout``
     - ``int``
     - Timeout in seconds for HTTP requests. Default: ``30``.
   * - ``retry_count``
     - ``int``
     - Number of retry attempts on failure. Default: ``0``.
   * - ``retry_delay``
     - ``float``
     - Delay in seconds between retries. Default: ``1.0``.

Examples
--------

Basic External API Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class MyInputFilter(InputFilter):
        user_id: int = field(required=True)

        is_active: bool = field(
            required=True,
            external_api={
                "url": "https://api.example.com/users/{{user_id}}/status",
                "method": "GET",
                "data_key": "is_active",
            }
        )

    # Example usage
    # Body: {"user_id": 123}

    @app.route("/test", methods=["GET"])
    @MyInputFilter.validate()
    def test_route():
        validated_data = g.validated_data
        print(validated_data["is_active"])  # True or False based on API response

Using Query Parameters
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    is_valid: bool = field(
        required=True,
        external_api={
            "url": "https://api.example.com/validate",
            "method": "GET",
            "params": {"user": "{{user_id}}", "hash": "{{hash}}"},
            "data_key": "is_valid",
        }
    )

This configuration sends the ``user_id`` and ``hash`` as query parameters, replacing the placeholders with validated data.

Handling Fallback Values
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    user_info: dict = field(
        required=True,
        fallback={"name": "unknown", "age": 0},
        external_api={
            "url": "https://api.example.com/user/{{user_id}}",
            "method": "GET",
            "data_key": "user",
        }
    )

Async Support
-------------

Installation
^^^^^^^^^^^^

To use async external APIs, install the optional async dependencies:

.. code-block:: bash

    pip install flask-inputfilter[async]

This installs ``httpx``, which is required for async HTTP requests.

Basic Async Usage
^^^^^^^^^^^^^^^^^

Enable async mode by setting ``async_mode=True`` in the ``ExternalApiConfig``.
The ``@validate()`` decorator automatically detects async routes and enables
parallel API execution.

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field
    from flask_inputfilter.models import ExternalApiConfig

    class UserFilter(InputFilter):
        user_id: int = field(
            required=True,
            external_api=ExternalApiConfig(
                url="https://api.example.com/users/{{user_id}}",
                method="GET",
                async_mode=True  # Enable async
            )
        )

    @app.route('/users', methods=['POST'])
    @UserFilter.validate()  # Auto-detects async route
    async def create_user():  # Note: async def
        data = g.validated_data
        return {"user": data}

Parallel API Calls
^^^^^^^^^^^^^^^^^^

When multiple fields have async external APIs, all API calls execute in parallel,
dramatically reducing total request time.

.. code-block:: python

    class OrderFilter(InputFilter):
        user_id: int = field(
            required=True,
            external_api=ExternalApiConfig(
                url="https://api.users.com/{{user_id}}",
                method="GET",
                async_mode=True
            )
        )

        product_id: int = field(
            required=True,
            external_api=ExternalApiConfig(
                url="https://api.products.com/{{product_id}}",
                method="GET",
                async_mode=True
            )
        )

        shipping_id: int = field(
            required=True,
            external_api=ExternalApiConfig(
                url="https://api.shipping.com/{{shipping_id}}",
                method="GET",
                async_mode=True
            )
        )

    @app.route('/orders', methods=['POST'])
    @OrderFilter.validate()
    async def create_order():
        # All 3 API calls execute in parallel!
        # Total time = max(user_api, product_api, shipping_api)
        return g.validated_data

Retry Logic
^^^^^^^^^^^

Configure retry behavior for unreliable APIs:

.. code-block:: python

    user_id: int = field(
        required=True,
        external_api=ExternalApiConfig(
            url="https://flaky-api.com/users/{{user_id}}",
            method="GET",
            async_mode=True,
            retry_count=3,      # Retry up to 3 times
            retry_delay=0.5     # Wait 500ms between retries
        )
    )

Custom Timeout
^^^^^^^^^^^^^^

Override the default 30-second timeout:

.. code-block:: python

    user_id: int = field(
        required=True,
        external_api=ExternalApiConfig(
            url="https://slow-api.com/users/{{user_id}}",
            method="GET",
            async_mode=True,
            timeout=60  # 60 seconds
        )
    )

Mixed Sync and Async
^^^^^^^^^^^^^^^^^^^^

You can mix sync and async external APIs in the same filter:

.. code-block:: python

    class MixedFilter(InputFilter):
        # Legacy sync API
        legacy_id: int = field(
            external_api=ExternalApiConfig(
                url="https://legacy-api.com/{{id}}",
                method="GET",
                async_mode=False  # Sync (default)
            )
        )

        # Modern async API
        modern_id: int = field(
            external_api=ExternalApiConfig(
                url="https://modern-api.com/{{id}}",
                method="GET",
                async_mode=True  # Async
            )
        )

    @app.route('/data', methods=['POST'])
    @UserFilter.validate()
    async def get_data():
        return g.validated_data

Error Handling
--------------

- **ValidationError** is raised when:
  - The API call returns a non-200 status code.
  - A required field is missing and no fallback/default is provided.
  - Validation of the field value fails.

Best Practices
--------------

- **Required Fields:** Clearly define required fields and provide fallback values where necessary.
- **Placeholders:** Ensure placeholders in URLs and parameters match the keys in ``validated_data``.
- **Fallbacks:** Always provide fallback values for critical fields to avoid disruptions in case of API failure.
- **Security:** Use HTTPS for API calls and secure sensitive data like API keys.

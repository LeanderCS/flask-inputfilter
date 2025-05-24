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

The external API functionality is configured via the ``external_api`` parameter in the ``add`` method. This parameter accepts a dictionary with the following structure:

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
     - ``Optional[Dict[str, str]]``
     - Query parameters for the API, with placeholders allowed.
   * - ``data_key``
     - ``Optional[str]``
     - Key in the JSON response to extract the required data.
   * - ``api_key``
     - ``Optional[str]``
     - API key for authorization, sent in the ``Authorization`` header.

Examples
--------

Basic External API Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class MyInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add(
                "user_id", required=True
            )

            self.add(
                "is_active",
                required=True,
                external_api={
                    "url": "https://api.example.com/users/{{user_id}}/status",
                    "method": "GET",
                    "data_key": "is_active",
                },
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

    self.add(
        "is_valid",
        required=True,
        external_api={
            "url": "https://api.example.com/validate",
            "method": "GET",
            "params": {"user": "{{user_id}}", "hash": "{{hash}}"},
            "data_key": "is_valid",
        },
    )

This configuration sends the ``user_id`` and ``hash`` as query parameters, replacing the placeholders with validated data.

Handling Fallback Values
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    self.add(
        "user_info",
        required=True,
        fallback={"name": "unknown", "age": 0},
        external_api={
            "url": "https://api.example.com/user/{{user_id}}",
            "method": "GET",
            "data_key": "user",
        },
    )

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

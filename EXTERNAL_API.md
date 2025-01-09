# External API Functionality in `InputFilter`

This documentation provides a comprehensive overview of the external API functionality available in the `InputFilter` class. It covers the configuration, core methods, and examples of usage for interacting with external APIs.

---

## 1. Overview

The `InputFilter` class includes a mechanism for fetching data from external APIs during the input validation process. 
This feature allows dynamic data retrieval based on user inputs, such as validating fields or fetching related data from an external service.

Important to know, the external api functionality runs after all other filters and validators have been executed.
This means that the data fetched from the external API will not be validated or filtered.

---

## 2. Configuration

The external API functionality is configured via the `external_api` parameter in the `add` method. This parameter accepts a dictionary with the following structure:

### `ExternalApiConfig` Fields

| Field      | Type                     | Description                                                                 |
|------------|--------------------------|-----------------------------------------------------------------------------|
| `url`      | `str`                    | The URL of the external API, with optional placeholders in `{{}}` format.  |
| `method`   | `str`                    | The HTTP method to use (e.g., `GET`, `POST`).                              |
| `params`   | `Optional[Dict[str, str]]` | Query parameters for the API, with placeholders allowed.                   |
| `data_key` | `Optional[str]`          | Key in the JSON response to extract the required data.                     |
| `api_key`  | `Optional[str]`          | API key for authorization, sent in the `Authorization` header.            |

---

## 3. Examples

### 3.1 Basic External API Integration

```python
from flask_inputfilter.InputFilter import InputFilter

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
filter_instance = MyInputFilter()
validated_data = filter_instance.validateData({"user_id": 123})
print(validated_data["is_active"])  # True or False based on API response
```

### 3.2 Using Query Parameters

```python
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
```

This configuration sends the `user_id` and `hash` as query parameters, replacing the placeholders with validated data.

---

### 3.3 Handling Fallback Values

If the external API call fails, a fallback value can be specified:

```python
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
```

---

## 4. Error Handling

- `ValidationError` is raised when:
  - The API call returns a non-200 status code.
  - A required field is missing and no fallback/default is provided.
  - Validation of the field value fails.

---

## 7. Best Practices

- **Required Fields:** Clearly define required fields and provide fallback values where necessary.
- **Placeholders:** Ensure placeholders in URLs and parameters match the keys in `validated_data`.
- **Fallbacks:** Always provide fallback values for critical fields to avoid disruptions in case of API failure.
- **Security:** Use HTTPS for API calls and secure sensitive data like API keys.
- **Testing:** Mock external API calls during unit testing to avoid dependencies on external systems.

---

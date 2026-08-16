# Flask-InputFilter Example Application

This example demonstrates various use cases of the Flask-InputFilter package,
showing how to implement input validation and filtering in a Flask application.

## Project Structure

```
example 1/
├── app.py                        # Main Flask application
├── filters/                      # InputFilter classes
│   ├── __init__.py               # Package exports
│   ├── product_inputfilter.py    # Product input validation
│   ├── profile_inputfilter.py    # Profile input validation
│   └── user_inputfilter.py       # User input validation
├── test.http                     # HTTP test requests
└── README.md                     # This file
```

## Setup

1. Make sure you have Flask and Flask-InputFilter installed:
```bash
  pip install flask flask-inputfilter
```

2. Run the example application:
```bash
  python app.py
```

The server will start on `http://localhost:5000`.

## Testing the Endpoints

You can use the provided `test.http` file to test the endpoints.
This file contains example requests for both successful and error cases.

### Available Endpoints

1. `POST /api/user`
   - Creates a new user
   - Required fields: name, age, email
   - Uses StringTrimFilter and ToIntegerFilter for data cleaning

2. `POST /api/profile`
   - Creates a new profile with nested user and address information
   - Demonstrates nested filtering with multiple InputFilter classes
   - Optional phone number field

3. `POST /api/product`
   - Creates a new product
   - Demonstrates list validation for tags
   - Required fields: name, price
   - Optional tags field as a list of strings

## Example Requests

### Successful User Creation
```json
{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com"
}
```

### Successful Profile Creation
```json
{
    "user": {
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com"
    },
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zip_code": 10001
    },
    "phone": "+1234567890"
}
```

### Successful Product Creation
```json
{
    "name": "Laptop",
    "price": 999,
    "tags": [
        "electronics",
        "sports"
    ]
}
```

## Key Features

1. **Modular Organization**
   - Easy to maintain and reuse
   - Clear separation of concerns

2. **Decorator-based Validation**
   - Use `@InputFilter.validate()` to automatically validate request data
   - Access validated data through Flask's `g.validated_data`

3. **Field Configuration**
   - Add fields using `field()`
   - Configure required fields and filters

4. **Error Handling**
   - Automatic 400 responses for validation errors
   - Detailed error messages in JSON format

## Best Practices

1. Chain filters when multiple transformations are needed

## Error Handling

The application demonstrates various validation errors:
- Missing required fields
- Invalid email format
- Invalid age format (must be integer)
- Invalid price format
- Invalid tags format (must be a list of strings)
- Invalid nested data structures

Each error will return a 400 status code with a descriptive error message. 
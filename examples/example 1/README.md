# Flask-InputFilter Example Application

This example demonstrates various use cases of the Flask-InputFilter package, showing how to implement input validation and filtering in a Flask application.

## Project Structure

```
example 1/
├── app.py                 # Main Flask application
├── filters/              # InputFilter classes
│   ├── __init__.py      # Package exports
│   ├── user_filter.py   # User input validation
│   ├── address_filter.py # Address input validation
│   ├── profile_filter.py # Profile input validation
│   └── product_filter.py # Product input validation
├── test.http            # HTTP test requests
└── README.md            # This file
```

## Features Demonstrated

1. Basic filtering with required fields
2. Nested filtering with complex objects
3. List filtering with type validation
4. Using the `@validate()` decorator for automatic validation
5. Modular filter organization

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

You can use the provided `test.http` file to test the endpoints. This file contains example requests for both successful and error cases.

### Available Endpoints

1. `POST /api/user`
   - Creates a new user
   - Required fields: name, age, email
   - Uses StringTrimFilter and ToIntegerFilter for data cleaning

2. `POST /api/profile`
   - Creates a new profile with nested user and address information
   - Demonstrates nested filtering with multiple InputFilter classes
   - Optional phone number field

3. `POST /api/products`
   - Creates a new product
   - Demonstrates basic type conversion with ToFloatFilter
   - Optional tags field

## Example Requests

### Successful User Creation
```json
{
    "name": "John Doe",
    "age": "30",
    "email": "john.doe@example.com"
}
```

### Successful Profile Creation
```json
{
    "user": {
        "name": "John Doe",
        "age": "30",
        "email": "john.doe@example.com"
    },
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zip_code": "10001"
    },
    "phone": "+1234567890"
}
```

### Successful Product Creation
```json
{
    "name": "Laptop",
    "price": "999.99",
    "tags": "electronics,computers,gadgets"
}
```

## Key Features

1. **Modular Organization**
   - Each InputFilter class in its own file
   - Easy to maintain and reuse
   - Clear separation of concerns

2. **Decorator-based Validation**
   - Use `@InputFilter.validate()` to automatically validate request data
   - Access validated data through Flask's `g.validated_data`

3. **Field Configuration**
   - Add fields in `__init__` using `self.add()`
   - Configure required fields and filters
   - Chain multiple filters for complex transformations

4. **Built-in Filters**
   - StringTrimFilter: Removes leading/trailing whitespace
   - ToIntegerFilter: Converts to integer
   - ToFloatFilter: Converts to float
   - ToStringFilter: Converts to string

5. **Error Handling**
   - Automatic 400 responses for validation errors
   - Detailed error messages in JSON format

## Best Practices

1. Organize InputFilter classes in separate files
2. Use `__init__.py` to expose filter classes
3. Always call `super().__init__()` in your InputFilter classes
4. Use appropriate filters for data type conversion
5. Chain filters when multiple transformations are needed
6. Use the `@validate()` decorator for automatic validation
7. Access validated data through `g.validated_data`

## Error Handling

The application demonstrates various validation errors:
- Missing required fields
- Invalid email format
- Invalid zip code format
- Invalid phone number format
- Negative price values
- Invalid data types

Each error will return a 400 status code with a descriptive error message. 
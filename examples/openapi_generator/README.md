# OpenAPI Generator Example

This example demonstrates how to use the OpenAPI generator to automatically create InputFilter classes from an OpenAPI specification.

## Files

- `api.yaml` - Example OpenAPI 3.0 specification
- `generated_filters.py` - Generated InputFilter classes (created by generator)

## Usage

### Using the CLI

Generate all schemas to a single file:

```bash
  flask-inputfilter generate openapi api.yaml --output generated_filters.py
```

Generate all schemas to separate files:

```bash
  flask-inputfilter generate openapi api.yaml --output-dir filters/
```

Generate a specific schema:

```bash
  flask-inputfilter generate openapi api.yaml --schema User --output user_filter.py
```

### Using the Python API

```python
from flask_inputfilter.generators.openapi import generate_from_openapi

# Generate all schemas
code = generate_from_openapi(
    openapi_file="api.yaml", output_file="generated_filters.py"
)

# Generate specific schema
code = generate_from_openapi(
    openapi_file="api.yaml", schema_name="User", output_file="user_filter.py"
)
```

## Example OpenAPI Schema

The `api.yaml` file contains example schemas including:

- **User** - Basic user schema with string, integer, boolean, and array fields
- **Product** - Product schema with nested objects and enums
- **Order** - Order schema with references to other schemas

## Generated Output

After running the generator, you'll get InputFilter classes that can be used directly in your Flask application:

```python
from generated_filters import UserInputFilter


@app.route("/users", methods=["POST"])
@UserInputFilter.validate()
def create_user():
    # Access validated data
    data = g.validated_data
    return jsonify(data), 201
```


# Flask InputFilter - AI Agent Guide

A Flask extension for validating and filtering input data with comprehensive type support.

## Quick Overview

Flask InputFilter provides a declarative way to validate and filter incoming data in Flask applications. It supports both traditional method-based and modern decorator-based field definitions with full type hints and Cython optimization.

## Installation

```bash
pip install flask-inputfilter
# or
uv add flask-inputfilter
# or
poetry add flask-inputfilter
```

## Core Concepts

### 1. InputFilter Classes
Create validation schemas by inheriting from `InputFilter`:

```python
from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field, global_filter
from flask_inputfilter.filters import ToIntegerFilter, StringTrimFilter
from flask_inputfilter.validators import IsIntegerValidator, LengthValidator

class UserInputFilter(InputFilter):
    # Modern decorator syntax (recommended)
    name: str = field(
        required=True,
        filters=[StringTrimFilter()],
        validators=[LengthValidator(min_length=2, max_length=50)]
    )

    age: int = field(
        required=True,
        filters=[ToIntegerFilter()],
        validators=[IsIntegerValidator()]
    )

    # Global filters/validators apply to all fields
    global_filter(StringTrimFilter())
```

### 2. Usage in Flask Routes

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    input_filter = UserInputFilter()
    input_filter.set_data(request.get_json())

    if not input_filter.is_valid():
        return jsonify({'errors': input_filter.get_error_messages()}), 400

    validated_data = input_filter.get_values()
    # Process validated_data...
    return jsonify(validated_data)
```

## Available Components

### Filters (Data Transformation)
- **String**: `ToUpperFilter`, `ToLowerFilter`, `StringTrimFilter`, `ToCamelCaseFilter`
- **Type Conversion**: `ToIntegerFilter`, `ToFloatFilter`, `ToBooleanFilter`, `ToDateFilter`
- **Data Structures**: `ToDataclassFilter`, `ToTypedDictFilter`, `ArrayExplodeFilter`
- **Images**: `ToBase64ImageFilter`, `ToImageFilter`, `Base64ImageResizeFilter`
- **Cleaning**: `ToAlphaNumericFilter`, `ToDigitsFilter`, `WhitelistFilter`, `BlacklistFilter`

### Validators (Data Validation)
- **Type Checking**: `IsStringValidator`, `IsIntegerValidator`, `IsFloatValidator`, `IsBooleanValidator`
- **Format**: `IsEmailValidator`, `IsUrlValidator`, `IsUuidValidator`, `IsJsonValidator`
- **Ranges**: `LengthValidator`, `RangeValidator`, `ArrayLengthValidator`
- **Dates**: `IsDateValidator`, `DateRangeValidator`, `IsFutureDateValidator`
- **Images**: `IsImageValidator`, `IsHorizontalImageValidator`, `IsVerticalImageValidator`
- **Logic**: `AndValidator`, `OrValidator`, `NotValidator`, `XorValidator`

### Conditions (Inter-field Validation)
- **Requirement**: `RequiredIfCondition`, `ExactlyOneOfCondition`
- **Logic**: `OneOfCondition`, `NOfCondition`, `ExactlyNOfCondition`
- **Comparison**: `EqualCondition`, `NotEqualCondition`

## Project Structure

```
flask_inputfilter/
├── __init__.py              # Main exports
├── input_filter.py          # Core InputFilter class
├── py.typed                 # PEP 561 type support
├── conditions/              # Inter-field validation logic
├── filters/                 # Data transformation components
├── validators/              # Data validation components
├── enums/                   # Predefined enums
├── exceptions/              # Custom exceptions
├── models/                  # Base classes and data models
├── mixins/                  # Reusable mixins
└── declarative/             # Decorator-based field definition
```

## Development Commands

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint code
ruff check

# Format code
ruff format

# Type checking
mypy flask_inputfilter

# Build documentation
cd docs && make html

# Build package
python -m build
```

## Advanced Features

### Custom Components
```python
from flask_inputfilter.models.base_filter import BaseFilter
from flask_inputfilter.models.base_validator import BaseValidator

class CustomFilter(BaseFilter):
    def filter(self, value, context=None):
        # Your transformation logic
        return transformed_value

class CustomValidator(BaseValidator):
    def is_valid(self, value, context=None):
        # Your validation logic
        return True  # or False
```

### External API Integration
```python
from flask_inputfilter.models.external_api_config import ExternalApiConfig

class UserInputFilter(InputFilter):
    user_id: int = field(
        external_api=ExternalApiConfig(
            url="https://api.example.com/users/{user_id}",
            method="GET",
            headers={"Authorization": "Bearer token"}
        )
    )
```

### Steps and Processing Order
```python
class ComplexInputFilter(InputFilter):
    data: dict = field(
        steps=[
            {'filters': [ToJsonFilter()]},
            {'validators': [IsJsonValidator()]},
            {'filters': [ToDataclassFilter(MyDataclass)]}
        ]
    )
```

## Type Support

- **Full PEP 561 compliance** with `py.typed` marker
- **Comprehensive type hints** in all modules
- **Stub files (.pyi)** for enhanced IDE support
- **Cython extensions** with type declarations
- **Compatible** with mypy, pyright, and other type checkers

## Performance

- **Cython optimization** available for performance-critical components
- **Optional compilation** with `pip install flask-inputfilter[compile]`
- **Fallback to Python** if compilation fails
- **Benchmarked performance** improvements in validation-heavy scenarios

## Documentation

- **Full Documentation**: https://leandercs.github.io/flask-inputfilter
- **API Reference**: Complete class and method documentation
- **Guides**: Step-by-step tutorials and best practices
- **Examples**: Real-world usage patterns

## Common Patterns

### API Endpoint Validation
```python
@app.route('/api/products', methods=['POST'])
def create_product():
    class ProductFilter(InputFilter):
        name: str = field(required=True, validators=[LengthValidator(1, 100)])
        price: float = field(required=True, filters=[ToFloatFilter()], validators=[RangeValidator(0.01, 10000)])
        category: str = field(validators=[InArrayValidator(['electronics', 'clothing', 'books'])])

    filter_instance = ProductFilter()
    filter_instance.set_data(request.get_json())

    if not filter_instance.is_valid():
        return jsonify({'errors': filter_instance.get_error_messages()}), 400

    return jsonify(filter_instance.get_values())
```

### Form Data Processing
```python
@app.route('/contact', methods=['POST'])
def contact_form():
    class ContactFilter(InputFilter):
        email: str = field(required=True, validators=[IsEmailValidator()])
        message: str = field(required=True, filters=[StringTrimFilter()], validators=[LengthValidator(10, 1000)])
        subscribe: bool = field(filters=[ToBooleanFilter()])

    # Process form data...
```

This guide provides AI agents with the essential context needed to effectively work with Flask InputFilter in any development scenario.
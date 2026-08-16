"""
Example: export InputFilter classes back to OpenAPI schemas.

Run from the repository root:

    python examples/openapi_generator/export_example.py
"""

from __future__ import annotations

import json

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.filters import ToIntegerFilter
from flask_inputfilter.generators.openapi import (
    to_openapi_components,
    to_openapi_schema,
)
from flask_inputfilter.validators import (
    IsEmailValidator,
    IsIntegerValidator,
    IsStringValidator,
    LengthValidator,
    RangeValidator,
)


class AddressInputFilter(InputFilter):
    street: str = field(required=True, validators=[IsStringValidator()])
    city: str = field(required=True, validators=[IsStringValidator()])


class UserInputFilter(InputFilter):
    name: str = field(
        required=True,
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=2, max_length=50),
        ],
    )
    email: str = field(required=True, validators=[IsEmailValidator()])
    age: int = field(
        filters=[ToIntegerFilter()],
        validators=[
            IsIntegerValidator(),
            RangeValidator(min_value=18, max_value=120),
        ],
    )
    address: dict = field(input_filter=AddressInputFilter)


if __name__ == "__main__":
    print("Single schema object:")
    print(json.dumps(to_openapi_schema(UserInputFilter), indent=2))

    print("\ncomponents/schemas document (nested filters become $refs):")
    print(json.dumps(to_openapi_components(UserInputFilter), indent=2))

import unittest
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsTypedDictValidator

from tests.validators import BaseValidatorTest

try:
    from typing import TypedDict
    TYPEDDICT_AVAILABLE = True
except ImportError:
    try:
        from typing_extensions import TypedDict
        TYPEDDICT_AVAILABLE = True
    except ImportError:
        TYPEDDICT_AVAILABLE = False

if TYPEDDICT_AVAILABLE:
    class User(TypedDict):
        id: int
else:
    # Fallback for when TypedDict is not available
    class User:
        __annotations__ = {"id": int}

        def __init__(self, id: int):
            self.id = id

        def __eq__(self, other):
            if isinstance(other, dict):
                return other == {"id": self.id}
            return NotImplemented


class TestIsTypedDictValidator(BaseValidatorTest):
    def test_valid_typed_dict(self):
        self.input_filter.add("data", validators=[IsTypedDictValidator(User)])
        self.input_filter.validate_data({"data": {"id": 123}})

    def test_invalid_typed_dict(self):
        self.input_filter.add("data", validators=[IsTypedDictValidator(User)])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"data": "not a dict"})

    def test_custom_error_message(self):
        self.input_filter.add(
            "data2",
            validators=[
                IsTypedDictValidator(
                    User, error_message="Custom error message"
                )
            ],
        )
        self.assertValidationError(
            "data2", "not a dict", "Custom error message"
        )

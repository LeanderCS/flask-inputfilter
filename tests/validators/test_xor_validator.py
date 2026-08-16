from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import (
    IsIntegerValidator,
    RangeValidator,
    XorValidator,
)
from tests.validators import BaseValidatorTest


class TestXorValidator(BaseValidatorTest):
    def test_valid_xor(self):
        self.input_filter.add(
            "age",
            validators=[
                XorValidator(
                    [IsIntegerValidator(), RangeValidator(max_value=10)]
                )
            ],
        )
        self.input_filter.validate_data({"age": 25})
        self.input_filter.validate_data({"age": 9.9})

    def test_invalid_xor(self):
        self.input_filter.add(
            "age",
            validators=[
                XorValidator(
                    [IsIntegerValidator(), RangeValidator(max_value=10)]
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"age": "not a number"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"age": 5})

    def test_custom_error_message(self):
        self.input_filter.add(
            "age",
            validators=[
                XorValidator(
                    [IsIntegerValidator(), RangeValidator(max_value=10)],
                    error_message="Custom error message",
                )
            ],
        )
        self.assertValidationError(
            "age", "not a number", "Custom error message"
        )
        self.assertValidationError("age", 5, "Custom error message")

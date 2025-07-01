from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import (
    IsFloatValidator,
    IsIntegerValidator,
    OrValidator,
)

from tests.validators import BaseValidatorTest


class TestOrValidator(BaseValidatorTest):
    def test_valid_or_integer_or_float(self):
        self.input_filter.add(
            "age",
            validators=[
                OrValidator([IsIntegerValidator(), IsFloatValidator()])
            ],
        )
        self.input_filter.validate_data({"age": 25})
        self.input_filter.validate_data({"age": 25.5})

    def test_invalid_or(self):
        self.input_filter.add(
            "age",
            validators=[
                OrValidator([IsIntegerValidator(), IsFloatValidator()])
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"age": "not a number"})

    def test_custom_error_message(self):
        self.input_filter.add(
            "age",
            validators=[
                OrValidator(
                    [IsIntegerValidator(), IsFloatValidator()],
                    error_message="Custom error message",
                )
            ],
        )
        self.assertValidationError(
            "age", "not a number", "Custom error message"
        )

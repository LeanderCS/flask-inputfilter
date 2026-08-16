from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsIntegerValidator, NotValidator
from tests.validators import BaseValidatorTest


class TestNotValidator(BaseValidatorTest):
    def test_valid_not_integer(self):
        self.input_filter.add(
            "age", validators=[NotValidator(IsIntegerValidator())]
        )
        self.input_filter.validate_data({"age": "not an integer"})

    def test_invalid_integer(self):
        self.input_filter.add(
            "age", validators=[NotValidator(IsIntegerValidator())]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"age": 25})

    def test_custom_error_message(self):
        self.input_filter.add(
            "age",
            validators=[
                NotValidator(
                    IsIntegerValidator(), error_message="Custom error message"
                )
            ],
        )
        self.input_filter.validate_data({"age": "not an integer"})
        self.assertValidationError("age", 25, "Custom error message")

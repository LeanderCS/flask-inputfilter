from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import LengthValidator
from tests.validators import BaseValidatorTest


class TestLengthValidator(BaseValidatorTest):
    def test_valid_length(self):
        self.input_filter.add(
            "name", validators=[LengthValidator(min_length=2, max_length=5)]
        )
        self.input_filter.validateData({"name": "test"})

    def test_invalid_length(self):
        self.input_filter.add(
            "name", validators=[LengthValidator(min_length=2, max_length=5)]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"name": "a"})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"name": "this_is_too_long"})

    def test_custom_error_message(self):
        self.input_filter.add(
            "name",
            validators=[
                LengthValidator(
                    min_length=2,
                    max_length=5,
                    error_message="Custom error message",
                )
            ],
        )
        self.assertValidationError(
            "name", "this_is_too_long", "Custom error message"
        )
        self.assertValidationError("name", "a", "Custom error message")

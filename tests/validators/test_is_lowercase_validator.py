from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsLowercaseValidator
from tests.validators import BaseValidatorTest


class TestIsLowercaseValidator(BaseValidatorTest):
    def test_valid_lowercase(self) -> None:
        self.input_filter.add("text", validators=[IsLowercaseValidator()])
        self.input_filter.validate_data({"text": "hello"})

    def test_invalid_lowercase(self) -> None:
        self.input_filter.add("text", validators=[IsLowercaseValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"text": "Hello"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "text2",
            validators=[IsLowercaseValidator(error_message="Custom error")],
        )
        self.assertValidationError("text2", "Hello", "Custom error")

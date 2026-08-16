from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsEmailValidator
from tests.validators import BaseValidatorTest


class TestIsEmailValidator(BaseValidatorTest):
    def test_valid_email(self) -> None:
        self.input_filter.add("email", validators=[IsEmailValidator()])
        self.input_filter.validate_data({"email": "john.doe@example.com"})
        self.input_filter.validate_data({"email": "user+tag@sub.example.org"})

    def test_invalid_email(self) -> None:
        self.input_filter.add("email", validators=[IsEmailValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"email": "not-an-email"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"email": "missing@tld"})

    def test_non_string_value(self) -> None:
        self.input_filter.add("email", validators=[IsEmailValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"email": 123})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "email",
            validators=[IsEmailValidator(error_message="Custom error")],
        )
        self.assertValidationError("email", "invalid", "Custom error")

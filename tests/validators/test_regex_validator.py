from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import RegexValidator

from tests.validators import BaseValidatorTest


class TestRegexValidator(BaseValidatorTest):
    def test_valid_regex(self):
        self.input_filter.add(
            "email", validators=[RegexValidator(RegexEnum.EMAIL.value)]
        )
        validated_data = self.input_filter.validate_data(
            {"email": "alice@example.com"}
        )
        self.assertEqual(validated_data["email"], "alice@example.com")

    def test_invalid_regex(self):
        self.input_filter.add(
            "email", validators=[RegexValidator(RegexEnum.EMAIL.value)]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"email": "invalid_email"})

    def test_custom_error_message(self):
        self.input_filter.add(
            "email",
            validators=[
                RegexValidator(
                    RegexEnum.EMAIL.value, error_message="Custom error message"
                )
            ],
        )
        self.assertValidationError(
            "email", "invalid_email", "Custom error message"
        )

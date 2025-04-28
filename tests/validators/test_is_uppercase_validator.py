from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsUppercaseValidator
from tests.validators import BaseValidatorTest


class TestIsUppercaseValidator(BaseValidatorTest):
    def test_valid_uppercase(self):
        self.input_filter.add("name", validators=[IsUppercaseValidator()])
        self.input_filter.validate_data({"name": "UPPERCASE"})

    def test_invalid_uppercase(self):
        self.input_filter.add("name", validators=[IsUppercaseValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"name": "NotUppercase"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"name": 100})

    def test_custom_error_message(self):
        self.input_filter.add(
            "name",
            validators=[
                IsUppercaseValidator(error_message="Custom error message")
            ],
        )
        self.assertValidationError(
            "name", "NotUppercase", "Custom error message"
        )

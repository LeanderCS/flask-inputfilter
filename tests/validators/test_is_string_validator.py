from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsStringValidator
from tests.validators import BaseValidatorTest


class TestIsStringValidator(BaseValidatorTest):
    def test_valid_string(self):
        self.input_filter.add("name", validators=[IsStringValidator()])
        self.input_filter.validate_data({"name": "obviously an string"})

    def test_invalid_string(self):
        self.input_filter.add("name", validators=[IsStringValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"name": 123})

    def test_custom_error_message(self):
        self.input_filter.add(
            "name",
            validators=[
                IsStringValidator(error_message="Custom error message")
            ],
        )
        self.assertValidationError("name", 123, "Custom error message")

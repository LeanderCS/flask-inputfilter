from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsUrlValidator
from tests.validators import BaseValidatorTest


class TestIsUrlValidator(BaseValidatorTest):
    def test_valid_url(self):
        self.input_filter.add("url", validators=[IsUrlValidator()])
        self.input_filter.validate_data({"url": "http://example.com"})

    def test_invalid_url(self):
        self.input_filter.add("url", validators=[IsUrlValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"url": "not_a_url"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"url": 100})

    def test_custom_error_message(self):
        self.input_filter.add(
            "url2",
            validators=[IsUrlValidator(error_message="Custom error message")],
        )
        self.assertValidationError("url2", "not_a_url", "Custom error message")

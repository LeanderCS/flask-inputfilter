from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsMimeTypeValidator
from tests.validators import BaseValidatorTest


class TestIsMimeTypeValidator(BaseValidatorTest):
    def test_valid_mime_type(self) -> None:
        self.input_filter.add("type", validators=[IsMimeTypeValidator()])
        self.input_filter.validate_data({"type": "image/png"})
        self.input_filter.validate_data({"type": "application/json"})
        self.input_filter.validate_data({"type": "image/svg+xml"})

    def test_invalid_mime_type(self) -> None:
        self.input_filter.add("type", validators=[IsMimeTypeValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"type": "not a mime type"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"type": "image"})

    def test_allowed_types(self) -> None:
        self.input_filter.add(
            "type",
            validators=[
                IsMimeTypeValidator(allowed_types=["image/png", "image/jpeg"])
            ],
        )
        self.input_filter.validate_data({"type": "image/png"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"type": "application/json"})

    def test_non_string_value(self) -> None:
        self.input_filter.add("type", validators=[IsMimeTypeValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"type": 42})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "type",
            validators=[IsMimeTypeValidator(error_message="Custom error")],
        )
        self.assertValidationError("type", "invalid", "Custom error")

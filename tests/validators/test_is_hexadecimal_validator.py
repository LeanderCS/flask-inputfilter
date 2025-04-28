from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsHexadecimalValidator
from tests.validators import BaseValidatorTest


class TestIsHexadecimalValidator(BaseValidatorTest):
    def test_valid_hexadecimal(self) -> None:
        self.input_filter.add("color", validators=[IsHexadecimalValidator()])
        self.input_filter.validate_data({"color": "FFAABB"})

    def test_invalid_hexadecimal(self) -> None:
        self.input_filter.add("color", validators=[IsHexadecimalValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"color": "NotHex"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "color2",
            validators=[
                IsHexadecimalValidator(error_message="Custom error message")
            ],
        )
        self.assertValidationError("color2", "NotHex", "Custom error message")

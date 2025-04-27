from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsRgbColorValidator
from tests.validators import BaseValidatorTest


class TestIsRgbColorValidator(BaseValidatorTest):
    def test_valid_rgb_color(self):
        self.input_filter.add("color", validators=[IsRgbColorValidator()])
        self.input_filter.validateData({"color": "rgb(125,125,125)"})
        self.input_filter.validateData({"color": "rgb(125, 125, 125)"})

    def test_invalid_rgb_color(self):
        self.input_filter.add("color", validators=[IsRgbColorValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"color": "not_a_color"})

    def test_custom_error_message(self):
        self.input_filter.add(
            "color2",
            validators=[
                IsRgbColorValidator(error_message="Custom error message")
            ],
        )
        self.assertValidationError(
            "color2", "not_a_color", "Custom error message"
        )

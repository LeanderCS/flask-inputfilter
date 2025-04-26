import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsHexadecimalValidator


class TestIsHexadecimalValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_hexadecimal(self) -> None:
        self.input_filter.add("color", validators=[IsHexadecimalValidator()])
        self.input_filter.validateData({"color": "FFAABB"})

    def test_invalid_hexadecimal(self) -> None:
        self.input_filter.add("color", validators=[IsHexadecimalValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"color": "NotHex"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "color2",
            validators=[
                IsHexadecimalValidator(error_message="Custom error message")
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"color2": "NotHex"})

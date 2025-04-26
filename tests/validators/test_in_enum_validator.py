import unittest
from enum import Enum

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import InEnumValidator


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class TestInEnumValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_enum_value(self) -> None:
        self.input_filter.add("color", validators=[InEnumValidator(Color)])
        self.input_filter.validateData({"color": "red"})

    def test_invalid_enum_value(self) -> None:
        self.input_filter.add("color", validators=[InEnumValidator(Color)])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"color": "yellow"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "custom_error2",
            validators=[
                InEnumValidator(Color, error_message="Custom error message")
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"custom_error2": "yellow"})

import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import ArrayLengthValidator


class TestArrayLengthValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_array_length(self) -> None:
        self.input_filter.add(
            "items",
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )
        self.input_filter.validateData({"items": [1, 2, 3, 4]})

    def test_invalid_too_short_array(self) -> None:
        self.input_filter.add(
            "items",
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"items": [1]})

    def test_invalid_too_long_array(self) -> None:
        self.input_filter.add(
            "items",
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"items": [1, 2, 3, 4, 5, 6]})

    def test_invalid_non_array_input(self) -> None:
        self.input_filter.add(
            "items",
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"items": "not an array"})

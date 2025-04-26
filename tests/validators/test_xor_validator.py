import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import (
    IsIntegerValidator,
    RangeValidator,
    XorValidator,
)


class TestXorValidator(unittest.TestCase):
    def setUp(self):
        self.input_filter = InputFilter()

    def test_valid_xor(self):
        self.input_filter.add(
            "age",
            validators=[
                XorValidator(
                    [IsIntegerValidator(), RangeValidator(max_value=10)]
                )
            ],
        )
        self.input_filter.validateData({"age": 25})
        self.input_filter.validateData({"age": 9.9})

    def test_invalid_xor(self):
        self.input_filter.add(
            "age",
            validators=[
                XorValidator(
                    [IsIntegerValidator(), RangeValidator(max_value=10)]
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": "not a number"})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": 5})

    def test_custom_error_message(self):
        self.input_filter.add(
            "age",
            validators=[
                XorValidator(
                    [IsIntegerValidator(), RangeValidator(max_value=10)],
                    error_message="Custom error message",
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": "not a number"})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": 5})

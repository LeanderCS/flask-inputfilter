import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import (
    IsFloatValidator,
    IsIntegerValidator,
    OrValidator,
)


class TestOrValidator(unittest.TestCase):
    def setUp(self):
        self.input_filter = InputFilter()

    def test_valid_or_integer_or_float(self):
        self.input_filter.add(
            "age",
            validators=[
                OrValidator([IsIntegerValidator(), IsFloatValidator()])
            ],
        )
        self.input_filter.validateData({"age": 25})
        self.input_filter.validateData({"age": 25.5})

    def test_invalid_or(self):
        self.input_filter.add(
            "age",
            validators=[
                OrValidator([IsIntegerValidator(), IsFloatValidator()])
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": "not a number"})

    def test_custom_error_message(self):
        self.input_filter.add(
            "age",
            validators=[
                OrValidator(
                    [IsIntegerValidator(), IsFloatValidator()],
                    error_message="Custom error message",
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": "not a number"})

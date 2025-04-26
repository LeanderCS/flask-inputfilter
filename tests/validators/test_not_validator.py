import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsIntegerValidator, NotValidator


class TestNotValidator(unittest.TestCase):
    def setUp(self):
        self.input_filter = InputFilter()

    def test_valid_not_integer(self):
        self.input_filter.add(
            "age", validators=[NotValidator(IsIntegerValidator())]
        )
        self.input_filter.validateData({"age": "not an integer"})

    def test_invalid_integer(self):
        self.input_filter.add(
            "age", validators=[NotValidator(IsIntegerValidator())]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": 25})

    def test_custom_error_message(self):
        self.input_filter.add(
            "age",
            validators=[
                NotValidator(
                    IsIntegerValidator(), error_message="Custom error message"
                )
            ],
        )
        self.input_filter.validateData({"age": "not an integer"})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": 25})

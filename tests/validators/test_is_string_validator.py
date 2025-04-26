import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsStringValidator


class TestIsStringValidator(unittest.TestCase):
    def setUp(self):
        self.input_filter = InputFilter()

    def test_valid_string(self):
        self.input_filter.add("name", validators=[IsStringValidator()])
        self.input_filter.validateData({"name": "obviously an string"})

    def test_invalid_string(self):
        self.input_filter.add("name", validators=[IsStringValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"name": 123})

    def test_custom_error_message(self):
        self.input_filter.add(
            "name",
            validators=[
                IsStringValidator(error_message="Custom error message")
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"name": 123})

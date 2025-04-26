import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsUppercaseValidator


class TestIsUppercaseValidator(unittest.TestCase):
    def setUp(self):
        self.input_filter = InputFilter()

    def test_valid_uppercase(self):
        self.input_filter.add("name", validators=[IsUppercaseValidator()])
        self.input_filter.validateData({"name": "UPPERCASE"})

    def test_invalid_uppercase(self):
        self.input_filter.add("name", validators=[IsUppercaseValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"name": "NotUppercase"})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"name": 100})

    def test_custom_error_message(self):
        self.input_filter.add(
            "name",
            validators=[
                IsUppercaseValidator(error_message="Custom error message")
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"name": "NotUppercase"})

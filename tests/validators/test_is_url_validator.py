import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsUrlValidator


class TestIsUrlValidator(unittest.TestCase):
    def setUp(self):
        self.input_filter = InputFilter()

    def test_valid_url(self):
        self.input_filter.add("url", validators=[IsUrlValidator()])
        self.input_filter.validateData({"url": "http://example.com"})

    def test_invalid_url(self):
        self.input_filter.add("url", validators=[IsUrlValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"url": "not_a_url"})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"url": 100})

    def test_custom_error_message(self):
        self.input_filter.add(
            "url2",
            validators=[IsUrlValidator(error_message="Custom error message")],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"url2": "not_a_url"})

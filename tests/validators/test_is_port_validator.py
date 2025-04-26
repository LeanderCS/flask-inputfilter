import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsPortValidator


class TestIsPortValidator(unittest.TestCase):
    def setUp(self):
        self.input_filter = InputFilter()

    def test_valid_port(self):
        self.input_filter.add("port", validators=[IsPortValidator()])
        self.input_filter.validateData({"port": 80})

    def test_invalid_port(self):
        self.input_filter.add("port", validators=[IsPortValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"port": 65536})

    def test_custom_error_message(self):
        self.input_filter.add(
            "port2",
            validators=[IsPortValidator(error_message="Custom error message")],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"port2": 65536})

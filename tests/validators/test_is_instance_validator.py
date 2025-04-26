import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsInstanceValidator


class TestIsInstanceValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_instance(self) -> None:
        self.input_filter.add("value", validators=[IsInstanceValidator(int)])
        self.input_filter.validateData({"value": 123})

    def test_invalid_instance(self) -> None:
        self.input_filter.add("value", validators=[IsInstanceValidator(int)])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"value": "not an int"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "value2",
            validators=[
                IsInstanceValidator(int, error_message="Custom error")
            ],
        )
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"value2": "not an int"})
        self.assertEqual(context.exception.args[0]["value2"], "Custom error")

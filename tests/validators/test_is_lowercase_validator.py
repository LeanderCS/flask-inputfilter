import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsLowercaseValidator


class TestIsLowercaseValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_lowercase(self) -> None:
        self.input_filter.add("text", validators=[IsLowercaseValidator()])
        self.input_filter.validateData({"text": "hello"})

    def test_invalid_lowercase(self) -> None:
        self.input_filter.add("text", validators=[IsLowercaseValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"text": "Hello"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "text2",
            validators=[IsLowercaseValidator(error_message="Custom error")],
        )
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"text2": "Hello"})
        self.assertEqual(context.exception.args[0]["text2"], "Custom error")

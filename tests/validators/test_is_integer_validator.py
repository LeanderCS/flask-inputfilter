import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsIntegerValidator


class TestIsIntegerValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_integer(self) -> None:
        self.input_filter.add("age", validators=[IsIntegerValidator()])
        self.input_filter.validateData({"age": 25})

    def test_invalid_integer(self) -> None:
        self.input_filter.add("age", validators=[IsIntegerValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": "not a number"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "age2",
            validators=[IsIntegerValidator(error_message="Custom error")],
        )
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"age2": "not a number"})
        self.assertEqual(context.exception.args[0]["age2"], "Custom error")

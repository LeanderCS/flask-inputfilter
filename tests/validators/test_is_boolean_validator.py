import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsBooleanValidator


class TestIsBooleanValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_boolean(self) -> None:
        self.input_filter.add("flag", validators=[IsBooleanValidator()])
        self.input_filter.validateData({"flag": True})

    def test_invalid_boolean(self) -> None:
        self.input_filter.add("flag", validators=[IsBooleanValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"flag": "yes"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "flag2",
            validators=[IsBooleanValidator(error_message="Custom error")],
        )
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"flag2": "notbool"})
        self.assertEqual(context.exception.args[0]["flag2"], "Custom error")

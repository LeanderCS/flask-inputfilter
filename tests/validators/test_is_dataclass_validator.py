import unittest
from dataclasses import dataclass

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsDataclassValidator


@dataclass
class User:
    id: int


class TestIsDataclassValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_dataclass(self) -> None:
        self.input_filter.add("data", validators=[IsDataclassValidator(User)])
        self.input_filter.validateData({"data": {"id": 1}})

    def test_invalid_dataclass(self) -> None:
        self.input_filter.add("data", validators=[IsDataclassValidator(User)])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"data": "not_dict"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "data2",
            validators=[
                IsDataclassValidator(User, error_message="Custom error")
            ],
        )
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"data2": "wrong"})
        self.assertEqual(context.exception.args[0]["data2"], "Custom error")

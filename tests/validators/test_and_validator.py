import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import (
    AndValidator,
    IsIntegerValidator,
    RangeValidator,
)


class TestAndValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_when_all_validators_pass(self) -> None:
        self.input_filter.add(
            "age",
            validators=[
                AndValidator(
                    [IsIntegerValidator(), RangeValidator(min_value=5)]
                )
            ],
        )
        self.input_filter.validateData({"age": 25})

    def test_invalid_when_first_validator_fails(self) -> None:
        self.input_filter.add(
            "age",
            validators=[
                AndValidator(
                    [IsIntegerValidator(), RangeValidator(min_value=5)]
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": "not a number"})

    def test_invalid_when_second_validator_fails(self) -> None:
        self.input_filter.add(
            "age",
            validators=[
                AndValidator(
                    [IsIntegerValidator(), RangeValidator(min_value=5)]
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": 4})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "age",
            validators=[
                AndValidator(
                    [IsIntegerValidator(), RangeValidator(min_value=5)],
                    error_message="Custom error message",
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"age": "not a number"})

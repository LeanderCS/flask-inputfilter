from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import (
    AndValidator,
    IsIntegerValidator,
    RangeValidator,
)

from tests.validators import BaseValidatorTest


class TestAndValidator(BaseValidatorTest):
    def test_valid_when_all_validators_pass(self) -> None:
        self.input_filter.add(
            "age",
            validators=[
                AndValidator(
                    [IsIntegerValidator(), RangeValidator(min_value=5)]
                )
            ],
        )
        self.input_filter.validate_data({"age": 25})

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
            self.input_filter.validate_data({"age": "not a number"})

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
            self.input_filter.validate_data({"age": 4})

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
        self.assertValidationError(
            "age", "not a number", "Custom error message"
        )

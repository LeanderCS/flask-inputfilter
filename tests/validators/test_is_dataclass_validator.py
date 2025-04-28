from dataclasses import dataclass

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsDataclassValidator
from tests.validators import BaseValidatorTest


@dataclass
class User:
    id: int


class TestIsDataclassValidator(BaseValidatorTest):
    def test_valid_dataclass(self) -> None:
        self.input_filter.add("data", validators=[IsDataclassValidator(User)])
        self.input_filter.validate_data({"data": {"id": 1}})

    def test_invalid_dataclass(self) -> None:
        self.input_filter.add("data", validators=[IsDataclassValidator(User)])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"data": "not_dict"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "data2",
            validators=[
                IsDataclassValidator(User, error_message="Custom error")
            ],
        )
        self.assertValidationError("data2", "wrong", "Custom error")

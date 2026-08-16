from dataclasses import dataclass
from typing import Optional

from flask_inputfilter.validators import IsDataclassValidator
from tests.validators import BaseValidatorTest


@dataclass
class User:
    id: int
    name: str = "Default Name"
    age: Optional[int] = None


@dataclass
class Profile:
    user: User
    address: str


class TestIsDataclassValidator(BaseValidatorTest):
    def test_valid_dataclass(self) -> None:
        self.input_filter.add("data", validators=[IsDataclassValidator(User)])
        self.input_filter.validate_data(
            {"data": {"id": 1, "name": "John", "age": 30}}
        )

    def test_missing_optional_field(self) -> None:
        self.input_filter.add("data", validators=[IsDataclassValidator(User)])
        self.input_filter.validate_data({"data": {"id": 1, "name": "John"}})

    def test_default_value(self) -> None:
        self.input_filter.add("data", validators=[IsDataclassValidator(User)])
        self.input_filter.validate_data({"data": {"id": 1}})

    def test_invalid_dataclass(self) -> None:
        self.input_filter.add("data", validators=[IsDataclassValidator(User)])
        self.assertValidationError("data", {"not_dict"})

    def test_invalid_field_type(self) -> None:
        self.input_filter.add("data", validators=[IsDataclassValidator(User)])
        self.assertValidationError("data", {"id": "invalid", "name": "John"})

    def test_nested_dataclass(self) -> None:
        self.input_filter.add(
            "data", validators=[IsDataclassValidator(Profile)]
        )
        self.input_filter.validate_data(
            {
                "data": {
                    "user": {"id": 1, "name": "John", "age": 30},
                    "address": "123 Main St",
                }
            }
        )

    def test_invalid_nested_dataclass(self) -> None:
        self.input_filter.add(
            "data", validators=[IsDataclassValidator(Profile)]
        )
        self.assertValidationError(
            "data",
            {
                "user": {"id": 1, "name": "John", "age": 30},
                "address": 123,
            },
        )

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "data",
            validators=[
                IsDataclassValidator(User, error_message="Custom error")
            ],
        )
        self.assertValidationError("data", "wrong", "Custom error")

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import ArrayLengthValidator

from tests.validators import BaseValidatorTest


class TestArrayLengthValidator(BaseValidatorTest):
    def setUp(self) -> None:
        super().setUp()

    def test_valid_array_length(self) -> None:
        self.input_filter.add(
            "items",
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )
        self.input_filter.validate_data({"items": [1, 2, 3, 4]})

    def test_invalid_too_short_array(self) -> None:
        self.input_filter.add(
            "items",
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"items": [1]})

    def test_invalid_too_long_array(self) -> None:
        self.input_filter.add(
            "items",
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"items": [1, 2, 3, 4, 5, 6]})

    def test_invalid_non_array_input(self) -> None:
        self.input_filter.add(
            "items",
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )
        self.assertValidationError(
            "items", "not an array", "Value 'not an array' must be a list."
        )

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "items",
            validators=[
                ArrayLengthValidator(
                    min_length=2,
                    max_length=5,
                    error_message="Custom error message",
                )
            ],
        )
        self.assertValidationError(
            "items", ["not an array"], "Custom error message"
        )

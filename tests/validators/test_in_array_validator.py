from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import InArrayValidator

from tests.validators import BaseValidatorTest


class TestInArrayValidator(BaseValidatorTest):
    def test_valid_in_array(self) -> None:
        self.input_filter.add(
            "color", validators=[InArrayValidator(["red", "green", "blue"])]
        )
        self.input_filter.validate_data({"color": "red"})

    def test_invalid_not_in_array(self) -> None:
        self.input_filter.add(
            "color", validators=[InArrayValidator(["red", "green", "blue"])]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"color": "yellow"})

    def test_strict_mode_validation(self) -> None:
        self.input_filter.add(
            "color_strict",
            validators=[
                InArrayValidator(["red", "green", "blue"], strict=True)
            ],
        )
        self.input_filter.validate_data({"color_strict": "red"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"color_strict": 1})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "custom_error2",
            validators=[
                InArrayValidator(
                    ["red", "green", "blue"],
                    error_message="Custom error message",
                )
            ],
        )
        self.assertValidationError(
            "custom_error2", "yellow", "Custom error message"
        )

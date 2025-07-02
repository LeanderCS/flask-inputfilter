from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsFloatValidator

from tests.validators import BaseValidatorTest


class TestIsFloatValidator(BaseValidatorTest):
    def test_valid_float(self) -> None:
        self.input_filter.add("price", validators=[IsFloatValidator()])
        self.input_filter.validate_data({"price": 19.99})

    def test_invalid_float(self) -> None:
        self.input_filter.add("price", validators=[IsFloatValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"price": "not_a_float"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "price2",
            validators=[
                IsFloatValidator(error_message="Custom error message")
            ],
        )
        self.assertValidationError(
            "price2", "not_a_float", "Custom error message"
        )

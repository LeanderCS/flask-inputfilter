from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import FloatPrecisionValidator
from tests.validators import BaseValidatorTest


class TestFloatPrecisionValidator(BaseValidatorTest):
    def test_valid_float_precision(self) -> None:
        self.input_filter.add(
            "price", validators=[FloatPrecisionValidator(precision=5, scale=2)]
        )
        self.input_filter.validate_data({"price": 19.99})

    def test_invalid_float_precision_and_scale(self) -> None:
        self.input_filter.add(
            "price", validators=[FloatPrecisionValidator(precision=5, scale=2)]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"price": 19.999})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"price": 1999.99})

    def test_invalid_not_a_float(self) -> None:
        self.input_filter.add(
            "price", validators=[FloatPrecisionValidator(precision=5, scale=2)]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"price": "not a float"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"price": float("inf")})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "custom_message2",
            validators=[
                FloatPrecisionValidator(
                    precision=5, scale=2, error_message="Custom error message"
                )
            ],
        )
        self.assertValidationError(
            "custom_message2", 19.999, "Custom error message"
        )

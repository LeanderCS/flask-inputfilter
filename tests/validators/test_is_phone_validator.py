from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsPhoneValidator
from tests.validators import BaseValidatorTest


class TestIsPhoneValidator(BaseValidatorTest):
    def test_valid_phone(self) -> None:
        self.input_filter.add("phone", validators=[IsPhoneValidator()])
        self.input_filter.validate_data({"phone": "+49 170 1234567"})
        self.input_filter.validate_data({"phone": "(030) 123-4567"})
        self.input_filter.validate_data({"phone": "1234567"})

    def test_invalid_phone(self) -> None:
        self.input_filter.add("phone", validators=[IsPhoneValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"phone": "12345"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"phone": "phone number"})

    def test_non_string_value(self) -> None:
        self.input_filter.add("phone", validators=[IsPhoneValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"phone": 1234567})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "phone",
            validators=[IsPhoneValidator(error_message="Custom error")],
        )
        self.assertValidationError("phone", "invalid", "Custom error")

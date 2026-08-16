from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsCreditCardValidator
from tests.validators import BaseValidatorTest


class TestIsCreditCardValidator(BaseValidatorTest):
    def test_valid_card_numbers(self) -> None:
        self.input_filter.add("card", validators=[IsCreditCardValidator()])
        self.input_filter.validate_data({"card": "4111111111111111"})
        self.input_filter.validate_data({"card": "5500005555555559"})
        self.input_filter.validate_data({"card": "371449635398431"})

    def test_valid_card_with_separators(self) -> None:
        self.input_filter.add("card", validators=[IsCreditCardValidator()])
        self.input_filter.validate_data({"card": "4111 1111 1111 1111"})
        self.input_filter.validate_data({"card": "4111-1111-1111-1111"})

    def test_invalid_luhn_checksum(self) -> None:
        self.input_filter.add("card", validators=[IsCreditCardValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"card": "4111111111111112"})

    def test_invalid_format(self) -> None:
        self.input_filter.add("card", validators=[IsCreditCardValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"card": "1234567890123456"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"card": "not a card"})

    def test_non_string_value(self) -> None:
        self.input_filter.add("card", validators=[IsCreditCardValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"card": 4111111111111111})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "card",
            validators=[IsCreditCardValidator(error_message="Custom error")],
        )
        self.assertValidationError("card", "invalid", "Custom error")

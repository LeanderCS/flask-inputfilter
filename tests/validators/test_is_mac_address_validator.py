from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsMacAddressValidator
from tests.validators import BaseValidatorTest


class TestIsMacAddressValidator(BaseValidatorTest):
    def test_valid_mac_address(self) -> None:
        self.input_filter.add("mac", validators=[IsMacAddressValidator()])
        self.input_filter.validateData({"mac": "00:14:22:01:23:45"})

    def test_invalid_mac_address(self) -> None:
        self.input_filter.add("mac", validators=[IsMacAddressValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"mac": "invalid mac"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "mac2",
            validators=[IsMacAddressValidator(error_message="Custom error")],
        )
        self.assertValidationError("mac2", "invalid", "Custom error")

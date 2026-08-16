from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsIpAddressValidator
from tests.validators import BaseValidatorTest


class TestIsIpAddressValidator(BaseValidatorTest):
    def test_valid_ipv4(self) -> None:
        self.input_filter.add("ip", validators=[IsIpAddressValidator()])
        self.input_filter.validate_data({"ip": "192.168.0.1"})

    def test_valid_ipv6(self) -> None:
        self.input_filter.add("ip", validators=[IsIpAddressValidator()])
        self.input_filter.validate_data({"ip": "2001:db8::1"})

    def test_invalid_ip(self) -> None:
        self.input_filter.add("ip", validators=[IsIpAddressValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"ip": "999.999.999.999"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"ip": "not an ip"})

    def test_version_restriction(self) -> None:
        self.input_filter.add(
            "ip", validators=[IsIpAddressValidator(version=4)]
        )
        self.input_filter.validate_data({"ip": "10.0.0.1"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"ip": "2001:db8::1"})

    def test_invalid_version_parameter(self) -> None:
        with self.assertRaises(ValueError):
            IsIpAddressValidator(version=5)

    def test_non_string_value(self) -> None:
        self.input_filter.add("ip", validators=[IsIpAddressValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"ip": 123})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "ip",
            validators=[IsIpAddressValidator(error_message="Custom error")],
        )
        self.assertValidationError("ip", "invalid", "Custom error")

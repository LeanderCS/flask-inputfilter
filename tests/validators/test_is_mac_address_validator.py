import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsMacAddressValidator


class TestIsMacAddressValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

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
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"mac2": "invalid"})
        self.assertEqual(context.exception.args[0]["mac2"], "Custom error")

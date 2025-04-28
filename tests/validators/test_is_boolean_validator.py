from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsBooleanValidator
from tests.validators import BaseValidatorTest


class TestIsBooleanValidator(BaseValidatorTest):
    def test_valid_boolean(self) -> None:
        self.input_filter.add("flag", validators=[IsBooleanValidator()])
        self.input_filter.validate_data({"flag": True})

    def test_invalid_boolean(self) -> None:
        self.input_filter.add("flag", validators=[IsBooleanValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"flag": "yes"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "flag2",
            validators=[IsBooleanValidator(error_message="Custom error")],
        )
        self.assertValidationError("flag2", "notbool", "Custom error")

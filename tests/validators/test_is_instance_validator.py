from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsInstanceValidator

from tests.validators import BaseValidatorTest


class TestIsInstanceValidator(BaseValidatorTest):
    def test_valid_instance(self) -> None:
        self.input_filter.add("value", validators=[IsInstanceValidator(int)])
        self.input_filter.validate_data({"value": 123})

    def test_invalid_instance(self) -> None:
        self.input_filter.add("value", validators=[IsInstanceValidator(int)])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"value": "not an int"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "value2",
            validators=[
                IsInstanceValidator(int, error_message="Custom error")
            ],
        )
        self.assertValidationError("value2", "not an int", "Custom error")

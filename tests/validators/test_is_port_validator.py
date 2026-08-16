from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsPortValidator
from tests.validators import BaseValidatorTest


class TestIsPortValidator(BaseValidatorTest):
    def test_valid_port(self):
        self.input_filter.add("port", validators=[IsPortValidator()])
        self.input_filter.validate_data({"port": 80})

    def test_invalid_port(self):
        self.input_filter.add("port", validators=[IsPortValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"port": 65536})

    def test_custom_error_message(self):
        self.input_filter.add(
            "port2",
            validators=[IsPortValidator(error_message="Custom error message")],
        )
        self.assertValidationError("port2", 65536, "Custom error message")

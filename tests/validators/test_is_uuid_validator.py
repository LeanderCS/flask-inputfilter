from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsUUIDValidator
from tests.validators import BaseValidatorTest


class TestIsUUIDValidator(BaseValidatorTest):
    def test_valid_uuid(self):
        self.input_filter.add("uuid", validators=[IsUUIDValidator()])
        self.input_filter.validateData(
            {"uuid": "550e8400-e29b-41d4-a716-446655440000"}
        )

    def test_invalid_uuid(self):
        self.input_filter.add("uuid", validators=[IsUUIDValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"uuid": "not_a_uuid"})

    def test_custom_error_message(self):
        self.input_filter.add(
            "uuid",
            validators=[IsUUIDValidator(error_message="Custom error message")],
        )
        self.assertValidationError(
            "uuid", "not_a_uuid", "Custom error message"
        )
        self.assertValidationError("uuid", 123, "Value must be a string.")

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsJsonValidator

from tests.validators import BaseValidatorTest


class TestIsJsonValidator(BaseValidatorTest):
    def test_valid_json(self) -> None:
        self.input_filter.add("data", validators=[IsJsonValidator()])
        self.input_filter.validate_data(
            {"data": '{"name": "Alice", "age": 25}'}
        )

    def test_invalid_json(self) -> None:
        self.input_filter.add("data", validators=[IsJsonValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"data": "not json"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "data2", validators=[IsJsonValidator(error_message="Custom error")]
        )
        self.assertValidationError("data2", "not json", "Custom error")

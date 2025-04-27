from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsArrayValidator
from tests.validators import BaseValidatorTest


class TestIsArrayValidator(BaseValidatorTest):
    def test_valid_array(self) -> None:
        self.input_filter.add("tags", validators=[IsArrayValidator()])
        self.input_filter.validateData({"tags": ["tag1", "tag2"]})

    def test_invalid_not_array(self) -> None:
        self.input_filter.add("tags", validators=[IsArrayValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"tags": "not_an_array"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "tags2",
            validators=[
                IsArrayValidator(error_message="Custom error message")
            ],
        )
        self.assertValidationError(
            "tags2", "not_an_array", "Custom error message"
        )

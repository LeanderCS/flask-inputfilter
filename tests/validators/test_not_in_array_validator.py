from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import NotInArrayValidator
from tests.validators import BaseValidatorTest


class TestNotInArrayValidator(BaseValidatorTest):
    def test_valid_not_in_array(self):
        self.input_filter.add(
            "color", validators=[NotInArrayValidator(["red", "green", "blue"])]
        )
        self.input_filter.validateData({"color": "yellow"})

    def test_invalid_in_array(self):
        self.input_filter.add(
            "color", validators=[NotInArrayValidator(["red", "green", "blue"])]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"color": "red"})

    def test_custom_error_message(self):
        self.input_filter.add(
            "color",
            validators=[
                NotInArrayValidator(
                    ["red", "green", "blue"],
                    error_message="Custom error message",
                )
            ],
        )
        self.assertValidationError("color", "red", "Custom error message")

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import RangeValidator
from tests.validators import BaseValidatorTest


class TestRangeValidator(BaseValidatorTest):
    def test_valid_range(self):
        self.input_filter.add("range_field", validators=[RangeValidator(2, 5)])
        self.input_filter.validate_data({"range_field": 3.76})

    def test_invalid_range(self):
        self.input_filter.add("range_field", validators=[RangeValidator(2, 5)])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"range_field": 1.22})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"range_field": 7.89})

    def test_custom_error_message(self):
        self.input_filter.add(
            "range_field",
            validators=[
                RangeValidator(2, 5, error_message="Custom error message")
            ],
        )
        self.assertValidationError("range_field", 7.89, "Custom error message")

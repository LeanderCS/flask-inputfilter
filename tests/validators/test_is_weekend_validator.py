from datetime import date, datetime

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsWeekendValidator
from tests.validators import BaseValidatorTest


class TestIsWeekendValidator(BaseValidatorTest):
    def test_valid_weekend(self):
        self.input_filter.add("date", validators=[IsWeekendValidator()])
        self.input_filter.validate_data({"date": date(2021, 1, 2)})
        self.input_filter.validate_data({"date": datetime(2021, 1, 2, 11, 11)})
        self.input_filter.validate_data({"date": "2021-01-02T11:11:11"})

    def test_invalid_weekend(self):
        self.input_filter.add("date", validators=[IsWeekendValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"date": date(2021, 1, 1)})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"date": "not a date"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"date": False})

    def test_custom_error_message(self):
        self.input_filter.add(
            "date",
            validators=[
                IsWeekendValidator(error_message="Custom error message")
            ],
        )
        self.assertValidationError(
            "date", date(2021, 1, 1), "Custom error message"
        )

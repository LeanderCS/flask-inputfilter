from datetime import date, datetime

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsWeekdayValidator

from tests.validators import BaseValidatorTest


class TestIsWeekdayValidator(BaseValidatorTest):
    def test_valid_weekday(self):
        self.input_filter.add("date", validators=[IsWeekdayValidator()])
        self.input_filter.validate_data({"date": date(2021, 1, 1)})
        self.input_filter.validate_data({"date": datetime(2021, 1, 1, 11, 11)})
        self.input_filter.validate_data({"date": "2021-01-01T11:11:11"})

    def test_invalid_weekday(self):
        self.input_filter.add("date", validators=[IsWeekdayValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"date": date(2021, 1, 2)})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"date": "not a date"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"date": False})

    def test_custom_error_message(self):
        self.input_filter.add(
            "date",
            validators=[
                IsWeekdayValidator(error_message="Custom error message")
            ],
        )
        self.assertValidationError(
            "date", date(2021, 1, 2), "Custom error message"
        )

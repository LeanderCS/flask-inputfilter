from datetime import date, datetime, timedelta

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsPastDateValidator

from tests.validators import BaseValidatorTest


class TestIsPastDateValidator(BaseValidatorTest):
    def test_valid_past_date(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        self.input_filter.validate_data({"date": date(2020, 1, 1)})

    def test_valid_past_datetime(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        self.input_filter.validate_data(
            {"date": datetime(2020, 1, 1, 12, 0, 0)}
        )

    def test_valid_past_isodatetime(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        self.input_filter.validate_data({"date": "2020-01-01T12:00:00"})

    def test_invalid_past_date(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"date": (date.today() + timedelta(days=10))}
            )

    def test_invalid_past_datetime(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"date": datetime.now() + timedelta(days=10)}
            )

    def test_invalid_past_isodatetime(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"date": (datetime.now() + timedelta(days=10)).isoformat()}
            )

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "date2",
            validators=[IsPastDateValidator(error_message="Custom error")],
        )
        future_date = datetime.now() + timedelta(days=10)
        self.assertValidationError("date2", future_date, "Custom error")

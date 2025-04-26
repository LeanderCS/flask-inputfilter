import unittest
from datetime import date, datetime, timedelta

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsPastDateValidator


class TestIsPastDateValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_past_date(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        self.input_filter.validateData({"date": date(2020, 1, 1)})

    def test_valid_past_datetime(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        self.input_filter.validateData(
            {"date": datetime(2020, 1, 1, 12, 0, 0)}
        )

    def test_valid_past_isodatetime(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        self.input_filter.validateData({"date": "2020-01-01T12:00:00"})

    def test_invalid_past_date(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"date": (date.today() + timedelta(days=10))}
            )

    def test_invalid_past_datetime(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"date": datetime.now() + timedelta(days=10)}
            )

    def test_invalid_past_isodatetime(self) -> None:
        self.input_filter.add("date", validators=[IsPastDateValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"date": (datetime.now() + timedelta(days=10)).isoformat()}
            )

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "date2",
            validators=[IsPastDateValidator(error_message="Custom error")],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"date2": (datetime.now() + timedelta(days=10))}
            )

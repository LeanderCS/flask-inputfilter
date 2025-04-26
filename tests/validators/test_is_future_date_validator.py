import unittest
from datetime import date, datetime, timedelta

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsFutureDateValidator


class TestIsFutureDateValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_future_date(self) -> None:
        self.input_filter.add(
            "future_date", validators=[IsFutureDateValidator()]
        )
        self.input_filter.validateData(
            {"future_date": (date.today() + timedelta(days=1))}
        )

    def test_valid_future_datetime(self) -> None:
        self.input_filter.add(
            "future_datetime", validators=[IsFutureDateValidator()]
        )
        self.input_filter.validateData(
            {"future_datetime": (datetime.now() + timedelta(days=10))}
        )

    def test_valid_future_isoformat_date(self) -> None:
        self.input_filter.add(
            "future_date_iso", validators=[IsFutureDateValidator()]
        )
        self.input_filter.validateData(
            {"future_date_iso": (date.today() + timedelta(days=1)).isoformat()}
        )

    def test_invalid_not_future_date(self) -> None:
        self.input_filter.add(
            "future_date", validators=[IsFutureDateValidator()]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"future_date": date(2020, 1, 1)})

    def test_invalid_not_future_datetime(self) -> None:
        self.input_filter.add(
            "future_datetime", validators=[IsFutureDateValidator()]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"future_datetime": datetime(2020, 1, 1, 12, 0, 0)}
            )

    def test_invalid_not_future_isoformat_date(self) -> None:
        self.input_filter.add(
            "future_date_iso", validators=[IsFutureDateValidator()]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"future_date_iso": "2020-01-01T12:00:00"}
            )

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "future_date_custom",
            validators=[
                IsFutureDateValidator(error_message="Custom error message")
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {
                    "future_date_custom": (
                        date.today() - timedelta(days=1)
                    ).isoformat()
                }
            )

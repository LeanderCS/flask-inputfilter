from datetime import date, datetime

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import DateRangeValidator
from tests.validators import BaseValidatorTest


class TestDateRangeValidator(BaseValidatorTest):
    def test_valid_date_in_range(self) -> None:
        self.input_filter.add(
            "date",
            validators=[DateRangeValidator(max_date=date(2021, 12, 31))],
        )
        self.input_filter.validateData({"date": date(2021, 6, 1)})

    def test_invalid_date_out_of_range(self) -> None:
        self.input_filter.add(
            "date",
            validators=[DateRangeValidator(max_date=date(2021, 12, 31))],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": date(2022, 6, 1)})

    def test_datetime_min_date(self) -> None:
        self.input_filter.add(
            "datetime",
            validators=[
                DateRangeValidator(min_date=datetime(2021, 1, 1, 0, 0))
            ],
        )
        self.input_filter.validateData({"datetime": date(2021, 6, 1)})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"datetime": date(2020, 6, 1)})

    def test_iso_date_range(self) -> None:
        self.input_filter.add(
            "iso_date",
            validators=[
                DateRangeValidator(
                    min_date="2021-01-12T22:26:08.542945",
                    max_date="2021-01-24T22:26:08.542945",
                )
            ],
        )
        self.input_filter.validateData(
            {"iso_date": "2021-01-15T22:26:08.542945"}
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"iso_date": "2022-01-15T22:26:08.542945"}
            )

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "custom_error",
            validators=[
                DateRangeValidator(
                    max_date="2021-01-24T22:26:08.542945",
                    error_message="Custom error message",
                )
            ],
        )
        self.assertValidationError(
            "custom_error", "2022-12-31T23:59:59", "Custom error message"
        )

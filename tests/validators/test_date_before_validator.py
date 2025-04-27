from datetime import date, datetime

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import DateBeforeValidator
from tests.validators import BaseValidatorTest


class TestDateBeforeValidator(BaseValidatorTest):
    def test_valid_dates(self) -> None:
        self.input_filter.add(
            "date",
            validators=[
                DateBeforeValidator(reference_date=date(2021, 12, 31))
            ],
        )
        self.input_filter.validateData({"date": date(2021, 6, 1)})
        self.input_filter.validateData({"date": datetime(2021, 6, 1, 0, 0)})
        self.input_filter.validateData({"date": "2021-06-01T10:00:55"})

    def test_invalid_dates(self) -> None:
        self.input_filter.add(
            "date",
            validators=[
                DateBeforeValidator(reference_date=date(2021, 12, 31))
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": date(2022, 6, 1)})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"date": datetime(2022, 6, 1, 0, 54)}
            )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": "20"})

    def test_datetime_validation(self) -> None:
        self.input_filter.add(
            "datetime",
            validators=[
                DateBeforeValidator(
                    reference_date=datetime(2021, 12, 31, 0, 0)
                )
            ],
        )
        self.input_filter.validateData({"datetime": date(2021, 6, 1)})
        self.input_filter.validateData(
            {"datetime": datetime(2021, 6, 1, 12, 0)}
        )
        self.input_filter.validateData({"datetime": "2021-06-01T00:00:00"})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"datetime": date(2022, 6, 1)})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"datetime": datetime(2022, 6, 1, 0, 0)}
            )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"datetime": "2022-06-01T00:00:00"})

    def test_isodatetime_validation(self) -> None:
        self.input_filter.add(
            "isodatetime",
            validators=[
                DateBeforeValidator(reference_date="2021-12-31T00:00:00")
            ],
        )
        self.input_filter.validateData({"isodatetime": date(2021, 6, 1)})
        self.input_filter.validateData(
            {"isodatetime": datetime(2021, 6, 1, 12, 0)}
        )
        self.input_filter.validateData({"isodatetime": "2021-06-01T00:00:00"})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"isodatetime": date(2022, 6, 1)})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"isodatetime": datetime(2022, 6, 1, 10, 0)}
            )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"isodatetime": "2022-06-01T00:00:00"}
            )

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "custom_error",
            validators=[
                DateBeforeValidator(
                    reference_date="2021-12-31T00:00:00",
                    error_message="Custom error message",
                )
            ],
        )
        self.assertValidationError(
            "custom_error", "2022-06-01T00:00:00", "Custom error message"
        )

import unittest
from datetime import date, datetime

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import DateAfterValidator


class TestDateAfterValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_date_after_reference(self) -> None:
        self.input_filter.add(
            "date",
            validators=[DateAfterValidator(reference_date=date(2021, 1, 1))],
        )
        self.input_filter.validateData({"date": date(2021, 6, 1)})

    def test_valid_datetime_after_reference(self) -> None:
        self.input_filter.add(
            "datetime",
            validators=[
                DateAfterValidator(reference_date=datetime(2021, 1, 1, 0, 0))
            ],
        )
        self.input_filter.validateData(
            {"datetime": datetime(2021, 6, 1, 12, 0)}
        )

    def test_invalid_before_reference(self) -> None:
        self.input_filter.add(
            "date",
            validators=[DateAfterValidator(reference_date=date(2021, 1, 1))],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": date(2020, 12, 31)})

    def test_invalid_unparsable_date(self) -> None:
        self.input_filter.add(
            "date",
            validators=[
                DateAfterValidator(reference_date="2021-01-01T00:00:00")
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": "unparseable date"})

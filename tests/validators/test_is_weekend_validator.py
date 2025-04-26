import unittest
from datetime import date, datetime

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsWeekendValidator


class TestIsWeekendValidator(unittest.TestCase):
    def setUp(self):
        self.input_filter = InputFilter()

    def test_valid_weekend(self):
        self.input_filter.add("date", validators=[IsWeekendValidator()])
        self.input_filter.validateData({"date": date(2021, 1, 2)})
        self.input_filter.validateData({"date": datetime(2021, 1, 2, 11, 11)})
        self.input_filter.validateData({"date": "2021-01-02T11:11:11"})

    def test_invalid_weekend(self):
        self.input_filter.add("date", validators=[IsWeekendValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": date(2021, 1, 1)})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": "not a date"})
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": False})

    def test_custom_error_message(self):
        self.input_filter.add(
            "date",
            validators=[
                IsWeekendValidator(error_message="Custom error message")
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": date(2021, 1, 1)})

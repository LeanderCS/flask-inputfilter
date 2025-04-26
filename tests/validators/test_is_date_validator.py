import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import ToDateFilter
from flask_inputfilter.validators import IsDateValidator


class TestIsDateValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_date(self) -> None:
        self.input_filter.add(
            "date", filters=[ToDateFilter()], validators=[IsDateValidator()]
        )
        self.input_filter.validateData({"date": "2025-01-01"})

    def test_invalid_date(self) -> None:
        self.input_filter.add(
            "date", filters=[ToDateFilter()], validators=[IsDateValidator()]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"date": "not_a_date"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "date2",
            filters=[ToDateFilter()],
            validators=[IsDateValidator(error_message="Custom error")],
        )
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"date2": 123})
        self.assertEqual(context.exception.args[0]["date2"], "Custom error")

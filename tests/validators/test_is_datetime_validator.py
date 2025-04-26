import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import ToDateTimeFilter
from flask_inputfilter.validators import IsDateTimeValidator


class TestIsDateTimeValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_datetime(self) -> None:
        self.input_filter.add(
            "datetime",
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator()],
        )
        self.input_filter.validateData({"datetime": "2024-01-01T12:00:00"})

    def test_invalid_datetime(self) -> None:
        self.input_filter.add(
            "datetime",
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator()],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"datetime": "wrong"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "datetime2",
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator(error_message="Custom error")],
        )
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"datetime2": "invalid"})
        self.assertEqual(
            context.exception.args[0]["datetime2"], "Custom error"
        )

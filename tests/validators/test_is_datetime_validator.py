from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import ToDateTimeFilter
from flask_inputfilter.validators import IsDateTimeValidator

from tests.validators import BaseValidatorTest


class TestIsDateTimeValidator(BaseValidatorTest):
    def test_valid_datetime(self) -> None:
        self.input_filter.add(
            "datetime",
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator()],
        )
        self.input_filter.validate_data({"datetime": "2024-01-01T12:00:00"})

    def test_invalid_datetime(self) -> None:
        self.input_filter.add(
            "datetime",
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator()],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"datetime": "wrong"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "datetime2",
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator(error_message="Custom error")],
        )
        self.assertValidationError("datetime2", "invalid", "Custom error")

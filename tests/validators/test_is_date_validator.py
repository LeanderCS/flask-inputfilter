from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import ToDateFilter
from flask_inputfilter.validators import IsDateValidator
from tests.validators import BaseValidatorTest


class TestIsDateValidator(BaseValidatorTest):
    def test_valid_date(self) -> None:
        self.input_filter.add(
            "date", filters=[ToDateFilter()], validators=[IsDateValidator()]
        )
        self.input_filter.validate_data({"date": "2025-01-01"})

    def test_invalid_date(self) -> None:
        self.input_filter.add(
            "date", filters=[ToDateFilter()], validators=[IsDateValidator()]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"date": "not_a_date"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "date2",
            filters=[ToDateFilter()],
            validators=[IsDateValidator(error_message="Custom error")],
        )
        self.assertValidationError("date2", 123, "Custom error")

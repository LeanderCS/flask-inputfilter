from datetime import date, datetime
from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsFutureDateValidator(BaseValidator):
    """
    Validator that checks if a date is in the future.
    """

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_date = self._parse_date(value)

        if value_date <= datetime.now():
            raise ValidationError(
                self.error_message or f"Date '{value}' is not in the future."
            )

    def _parse_date(self, value: Any) -> datetime:
        """
        Converts a value to a datetime object.
        Supports ISO 8601 formatted strings and datetime objects.
        """

        if isinstance(value, datetime):
            return value

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid ISO 8601 format '{value}'.")

        raise ValidationError(
            f"Unsupported type for past date validation '{type(value)}'."
        )

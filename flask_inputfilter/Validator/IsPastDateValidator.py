from datetime import date, datetime
from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsPastDateValidator(BaseValidator):
    """
    Validator that checks if a date is in the past.
    """

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_datetime = self.__parse_date(value)

        if value_datetime >= datetime.now():
            raise ValidationError(
                self.error_message or f"Date '{value}' is not in the past."
            )

    @staticmethod
    def __parse_date(value: Any) -> datetime:
        """
        Converts a value to a datetime object.
        Supports ISO 8601 formatted strings and datetime objects.
        """

        if isinstance(value, datetime):
            return value

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid ISO 8601 format '{value}'.")

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        raise ValidationError(
            f"Unsupported type for past date validation '{type(value)}'."
        )

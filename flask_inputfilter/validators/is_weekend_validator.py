from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsWeekendValidator(BaseValidator):
    """
    Validator that checks if a date is on a weekend (Saturday or Sunday).
    Supports datetime and ISO 8601 formatted strings.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_datetime = self.__parse_date(value)

        if value_datetime.weekday() not in (5, 6):
            raise ValidationError(
                self.error_message or f"Date '{value}' is not on a weekend."
            )

    @staticmethod
    def __parse_date(value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid ISO 8601 format: {value}")

        raise ValidationError(
            f"Unsupported type for weekend validation: {type(value)}"
        )

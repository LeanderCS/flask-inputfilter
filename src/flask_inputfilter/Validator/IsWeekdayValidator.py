from datetime import datetime
from typing import Any

from ..Exception import ValidationError


class IsWeekdayValidator:
    """
    Validator that checks if a date is on a weekday (Monday to Friday).
    Supports datetime and ISO 8601 formatted strings.
    """

    def __init__(
        self, error_message: str = "Date '{}' is not a weekday."
    ) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_datetime = self._parse_date(value)

        if value_datetime.weekday() in (5, 6):
            if "{}" in self.error_message:
                raise ValidationError(self.error_message.format(value))

            raise ValidationError(self.error_message)

    def _parse_date(self, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid ISO 8601 format: {value}")

        else:
            raise ValidationError(
                f"Unsupported type for weekday validation: {type(value)}"
            )

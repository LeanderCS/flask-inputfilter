from datetime import date, datetime
from typing import Any, Optional

from ..Exception import ValidationError
from .BaseValidator import BaseValidator


class DateRangeValidator(BaseValidator):
    """
    Validator that checks if a date is within a specific range.
    """

    def __init__(
        self,
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
        error_message="Date '{}' is not in the range from '{}' to '{}'.",
    ) -> None:
        self.min_date = min_date
        self.max_date = max_date
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_date = self._parse_date(value)
        min_date = self._parse_date(self.min_date) if self.min_date else None
        max_date = self._parse_date(self.max_date) if self.max_date else None

        if (min_date and value_date < min_date) or (
            max_date and value_date > max_date
        ):
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(
                        value, self.min_date, self.max_date
                    )
                )

            raise ValidationError(self.error_message)

    def _parse_date(self, value: Any) -> datetime:
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
                raise ValidationError(f"Invalid ISO 8601 format: {value}")

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        else:
            raise ValidationError(
                f"Unsupported type for past date validation: {type(value)}"
            )

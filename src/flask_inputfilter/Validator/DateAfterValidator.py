from datetime import datetime
from typing import Any

from ..Exception import ValidationError


class DateAfterValidator:
    """
    Validator that checks if a date is after a specific date.
    Supports datetime and ISO 8601 formatted strings.
    """

    def __init__(
        self,
        reference_date: str,
        error_message: str = "Date '{}' is not after '{}'.",
    ) -> None:
        self.reference_date = datetime.fromisoformat(reference_date)
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_datetime = self._parse_date(value)

        if value_datetime <= self.reference_date:
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(value, self.reference_date)
                )

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
                f"Unsupported type for date comparison: {type(value)}"
            )

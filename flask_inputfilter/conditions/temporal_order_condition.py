from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict

from flask_inputfilter.conditions import BaseCondition
from flask_inputfilter.exceptions import ValidationError


class TemporalOrderCondition(BaseCondition):
    """
    Condition to check if the first date is before the second date.
    Supports datetime, date, and ISO 8601 formatted strings.
    """

    __slots__ = ("smaller_date_field", "larger_date_field")

    def __init__(
        self, smaller_date_field: str, larger_date_field: str
    ) -> None:
        self.smaller_date_field = smaller_date_field
        self.larger_date_field = larger_date_field

    def check(self, data: Dict[str, Any]) -> bool:
        smaller_date = self._parse_date(data.get(self.smaller_date_field))
        larger_date = self._parse_date(data.get(self.larger_date_field))

        return smaller_date < larger_date

    @staticmethod
    def _parse_date(value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid date format: {value}")

        raise ValidationError(
            f"Unsupported type for date parsing: {type(value)}"
        )

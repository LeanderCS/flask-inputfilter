from datetime import date, datetime
from typing import Any, Dict

from ..Exception import ValidationError
from .BaseCondition import BaseCondition


class TemporalOrderCondition(BaseCondition):
    """
    Condition to check if the first date is before the second date.
    Supports datetime, date, and ISO 8601 formatted strings.
    """

    def __init__(self, first_field: str, second_field: str) -> None:
        self.first_field = first_field
        self.second_field = second_field

    def check(self, data: Dict[str, Any]) -> bool:
        first_date = self._parse_date(data.get(self.first_field))
        second_date = self._parse_date(data.get(self.second_field))

        return first_date < second_date

    @staticmethod
    def _parse_date(value: Any) -> datetime:
        """
        Converts a value to a datetime object if possible.
        Supports datetime, date, and ISO 8601 strings.
        """

        if isinstance(value, datetime):
            return value

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid date format: {value}")

        else:
            raise ValidationError(
                f"Unsupported type for date parsing: {type(value)}"
            )

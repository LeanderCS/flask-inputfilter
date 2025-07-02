from __future__ import annotations

from datetime import date, datetime
from typing import Any

from flask_inputfilter.exceptions import ValidationError


def parse_date(value: Any) -> datetime:
    """
    Converts a value to a datetime object.

    Supports ISO 8601 formatted strings and datetime objects.
    """
    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)

        except ValueError:
            raise ValidationError(f"Invalid ISO 8601 format '{value}'.")

    raise ValidationError(
        f"Unsupported type for date comparison '{type(value)}'."
    )

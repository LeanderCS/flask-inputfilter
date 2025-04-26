from __future__ import annotations

from datetime import date, datetime
from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToDateFilter(BaseFilter):
    """
    Filter that converts a value to a date object.
    Supports ISO 8601 formatted strings and datetime objects.
    """

    def apply(self, value: Any) -> Union[date, Any]:
        if isinstance(value, datetime):
            return value.date()

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value).date()

            except ValueError:
                return value

        return value

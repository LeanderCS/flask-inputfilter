from __future__ import annotations

from datetime import date, datetime
from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToDateTimeFilter(BaseFilter):
    """
    Filter that converts a value to a datetime object.
    Supports ISO 8601 formatted strings.
    """

    def apply(self, value: Any) -> Union[datetime, Any]:
        if isinstance(value, datetime):
            return value

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                return value

        return value

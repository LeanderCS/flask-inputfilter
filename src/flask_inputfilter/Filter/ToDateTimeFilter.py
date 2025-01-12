from datetime import datetime
from typing import Any, Union

from .BaseFilter import BaseFilter


class ToDateTimeFilter(BaseFilter):
    """
    Filter that converts a value to a datetime object.
    Supports ISO 8601 formatted strings.
    """

    def apply(self, value: Any) -> Union[datetime, Any]:
        if isinstance(value, datetime):
            return value

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                return value

        else:
            return value

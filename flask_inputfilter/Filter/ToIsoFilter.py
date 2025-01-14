from datetime import date, datetime
from typing import Any, Union

from .BaseFilter import BaseFilter


class ToIsoFilter(BaseFilter):
    """
    Filter that converts a date or datetime to an ISO 8601 formatted string.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        if isinstance(value, datetime):
            return value.isoformat()

        elif isinstance(value, date):
            return value.isoformat()

        else:
            return value

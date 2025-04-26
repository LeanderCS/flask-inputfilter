from __future__ import annotations

from datetime import date, datetime
from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToIsoFilter(BaseFilter):
    """
    Filter that converts a date or datetime to an ISO 8601 formatted string.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        if isinstance(value, (datetime, date)):
            return value.isoformat()

        return value

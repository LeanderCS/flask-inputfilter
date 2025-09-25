from __future__ import annotations

from datetime import date, datetime
from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToDateFilter(BaseFilter):
    """
    Converts an input value to a ``date`` object. Supports ISO 8601 formatted
    strings and datetime objects.

    **Expected Behavior:**

    - If the input is a datetime, returns the date portion.
    - If the input is a string, attempts to parse it as an ISO 8601 date.
    - Returns the original value if conversion fails.

    **Example Usage:**

    .. code-block:: python

        class BirthdateFilter(InputFilter):
            birthdate: date = field(filters=[
                ToDateFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[date, Any]:
        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value).date()

            except ValueError:
                return value

        return value

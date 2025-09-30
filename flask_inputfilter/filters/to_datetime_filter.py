from __future__ import annotations

from datetime import date, datetime
from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToDateTimeFilter(BaseFilter):
    """
    Converts an input value to a ``datetime`` object. Supports ISO 8601
    formatted strings.

    **Expected Behavior:**

    - If the input is a datetime, it is returned unchanged.
    - If the input is a date, it is combined with a minimum time value.
    - If the input is a string, the filter attempts to parse it as an
      ISO 8601 datetime.
    - If conversion fails, the original value is returned.

    **Example Usage:**

    .. code-block:: python

        class TimestampFilter(InputFilter):
            timestamp = field(filters=[
                ToDateTimeFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[datetime, Any]:
        if isinstance(value, datetime):
            return value

        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                return value

        return value

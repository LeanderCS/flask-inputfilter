from __future__ import annotations

from datetime import date, datetime
from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToIsoFilter(BaseFilter):
    """
    Converts a date or datetime object to an ISO 8601 formatted string.

    **Expected Behavior:**

    - If the input is a date or datetime, returns its ISO 8601 string.
    - Otherwise, returns the original value.

    **Example Usage:**

    .. code-block:: python

        class TimestampIsoFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('timestamp', filters=[
                    ToIsoFilter()
                ])
    """

    def apply(self, value: Any) -> Union[str, Any]:
        if isinstance(value, (datetime, date)):
            return value.isoformat()

        return value

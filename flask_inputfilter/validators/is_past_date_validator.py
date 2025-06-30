from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.helpers import parse_date
from flask_inputfilter.validators import BaseValidator


class IsPastDateValidator(BaseValidator):
    """
    Checks whether a given date is in the past. Supports datetime objects, date
    objects, and ISO 8601 formatted strings.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the date
        is not in the past.

    **Expected Behavior:**

    Parses the input date and verifies that it is earlier than the current
    date and time. Raises a ``ValidationError`` if the input date is not
    in the past.

    **Example Usage:**

    .. code-block:: python

        class HistoryInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('past_date', validators=[
                    IsPastDateValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if parse_date(value) >= datetime.now():
            raise ValidationError(
                self.error_message or f"Date '{value}' is not in the past."
            )

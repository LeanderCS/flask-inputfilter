from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.helpers import parse_date
from flask_inputfilter.models import BaseValidator


class IsWeekdayValidator(BaseValidator):
    """
    Checks whether a given date falls on a weekday (Monday to Friday). Supports
    datetime objects, date objects, and ISO 8601 formatted strings.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      date is not a weekday.

    **Expected Behavior:**

    Parses the input date and verifies that it corresponds to a weekday.
    Raises a ``ValidationError`` if the date falls on a weekend.

    **Example Usage:**

    .. code-block:: python

        class WorkdayInputFilter(InputFilter):
            date = field(validators=[
                IsWeekdayValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if parse_date(value).weekday() in (5, 6):
            raise ValidationError(
                self.error_message or f"Date '{value}' is not a weekday."
            )

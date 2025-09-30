from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.helpers import parse_date
from flask_inputfilter.models import BaseValidator


class IsWeekendValidator(BaseValidator):
    """
    Validates that a given date falls on a weekend (Saturday or Sunday).
    Supports datetime objects, date objects, and ISO 8601 formatted strings.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      date is not on a weekend.

    **Expected Behavior:**

    Parses the input date and confirms that it corresponds to a weekend day.
    Raises a ``ValidationError`` if the date is on a weekday.

    **Example Usage:**

    .. code-block:: python

        class WeekendInputFilter(InputFilter):
            date = field(validators=[
                IsWeekendValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if parse_date(value).weekday() not in (5, 6):
            raise ValidationError(
                self.error_message or f"Date '{value}' is not on a weekend."
            )

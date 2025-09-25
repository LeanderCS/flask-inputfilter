from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.helpers import parse_date
from flask_inputfilter.models import BaseValidator

if TYPE_CHECKING:
    from datetime import date, datetime


class DateRangeValidator(BaseValidator):
    """
    Checks if a date falls within a specified range.

    **Parameters:**

    - **min_date** (*Optional[Union[str, date, datetime]]*): The lower bound
      of the date range.
    - **max_date** (*Optional[Union[str, date, datetime]]*): The upper bound
      of the date range.
    - **error_message** (*Optional[str]*): Custom error message if the date
      is outside the range.

    **Expected Behavior:**

    Ensures the input date is not earlier than ``min_date`` and not later
    than ``max_date``. A ``ValidationError`` is raised if the check fails.

    **Example Usage:**

    .. code-block:: python

        class BookingInputFilter(InputFilter):
            booking_date: str = field(validators=[
                DateRangeValidator(
                    min_date="2023-01-01",
                    max_date="2023-01-31"
                )
            ])
    """

    __slots__ = ("error_message", "max_date", "min_date")

    def __init__(
        self,
        min_date: Optional[Union[str, date, datetime]] = None,
        max_date: Optional[Union[str, date, datetime]] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.min_date = parse_date(min_date) if min_date else None
        self.max_date = parse_date(max_date) if max_date else None
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_date = parse_date(value)

        if (self.min_date and value_date < self.min_date) or (
            self.max_date and value_date > self.max_date
        ):
            raise ValidationError(
                self.error_message
                or f"Date '{value}' is not in the range from "
                f"'{self.min_date}' to '{self.max_date}'."
            )

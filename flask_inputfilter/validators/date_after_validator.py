from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.helpers import parse_date
from flask_inputfilter.models import BaseValidator

if TYPE_CHECKING:
    from datetime import date, datetime


class DateAfterValidator(BaseValidator):
    """
    Ensures that a given date is after a specified reference date. It supports
    both datetime objects and ISO 8601 formatted strings.

    **Parameters:**

    - **reference_date** (*Union[str, date, datetime]*): The date that the
      input must be later than.
    - **error_message** (*Optional[str]*): Custom error message if the
      validation fails.

    **Expected Behavior:**

    Converts both the input and the reference date to datetime objects and
    verifies that the input date is later. If the check fails, a
    ``ValidationError`` is raised.

    **Example Usage:**

    .. code-block:: python

        class EventInputFilter(InputFilter):
            event_date: str = field(validators=[
                DateAfterValidator(reference_date="2023-01-01")
            ])
    """

    __slots__ = ("error_message", "reference_date")

    def __init__(
        self,
        reference_date: Union[str, date, datetime],
        error_message: Optional[str] = None,
    ) -> None:
        self.reference_date = parse_date(reference_date)
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if parse_date(value) < self.reference_date:
            raise ValidationError(
                self.error_message
                or f"Date '{value}' is not after '{self.reference_date}'."
            )

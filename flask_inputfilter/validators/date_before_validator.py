from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.helpers import parse_date
from flask_inputfilter.models import BaseValidator

if TYPE_CHECKING:
    from datetime import date, datetime


class DateBeforeValidator(BaseValidator):
    """
    Validates that a given date is before a specified reference date. It
    supports datetime objects and ISO 8601 formatted strings.

    **Parameters:**

    - **reference_date** (*Union[str, date, datetime]*): The date that the
      input must be earlier than.
    - **error_message** (*Optional[str]*): Custom error message if validation
      fails.

    **Expected Behavior:**

    Parses the input and reference date into datetime objects and checks that
    the input date is earlier. Raises a ``ValidationError`` on failure.

    **Example Usage:**

    .. code-block:: python

        class RegistrationInputFilter(InputFilter):
            birth_date: str = field(validators=[
                DateBeforeValidator(reference_date="2005-01-01")
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
        if parse_date(value) >= self.reference_date:
            raise ValidationError(
                self.error_message
                or f"Date '{value}' is not before '{self.reference_date}'."
            )

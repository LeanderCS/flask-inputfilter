from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.helpers import parse_date
from flask_inputfilter.models import BaseValidator


class IsFutureDateValidator(BaseValidator):
    """
    Ensures that a given date is in the future. Supports datetime objects and
    ISO 8601 formatted strings.

    **Parameters:**

    - **tz** (*Optional[timezone]*, default: ``timezone.utc``): Timezone to
      use for comparison.
    - **error_message** (*Optional[str]*): Custom error message if the
      date is not in the future.

    **Expected Behavior:**

    Parses the input date and compares it to the current date and time. If
    the input date is not later than the current time, a ``ValidationError``
    is raised.

    **Example Usage:**

    .. code-block:: python

        class AppointmentInputFilter(InputFilter):
            appointment_date: str = field(validators=[
                IsFutureDateValidator()
            ])
    """

    __slots__ = ("error_message", "tz")

    def __init__(
        self,
        tz: Optional[timezone] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.tz = tz or timezone.utc
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        parsed_date = parse_date(value)
        current_time = datetime.now(self.tz)

        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=self.tz)

        if parsed_date <= current_time:
            raise ValidationError(
                self.error_message or f"Date '{value}' is not in the future."
            )

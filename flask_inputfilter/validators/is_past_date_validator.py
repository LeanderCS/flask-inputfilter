from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.helpers import parse_date
from flask_inputfilter.models import BaseValidator


class IsPastDateValidator(BaseValidator):
    """
    Checks whether a given date is in the past. Supports datetime objects, date
    objects, and ISO 8601 formatted strings.

    **Parameters:**

    - **tz** (*Optional[timezone]*, default: ``timezone.utc``): Timezone to
      use for comparison.
    - **error_message** (*Optional[str]*): Custom error message if the date
      is not in the past.

    **Expected Behavior:**

    Parses the input date and verifies that it is earlier than the current
    date and time. Raises a ``ValidationError`` if the input date is not
    in the past.

    **Example Usage:**

    .. code-block:: python

        class HistoryInputFilter(InputFilter):
            past_date = field(validators=[
                IsPastDateValidator()
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

        if parsed_date >= current_time:
            raise ValidationError(
                self.error_message or f"Date '{value}' is not in the past."
            )

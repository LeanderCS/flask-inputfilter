from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.helpers import parse_date
from flask_inputfilter.validators import BaseValidator


class IsFutureDateValidator(BaseValidator):
    """
    Ensures that a given date is in the future. Supports datetime objects and
    ISO 8601 formatted strings.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
        date is not in the future.

    **Expected Behavior:**

    Parses the input date and compares it to the current date and time. If
    the input date is not later than the current time, a ``ValidationError``
    is raised.

    **Example Usage:**

    .. code-block:: python

        class AppointmentInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('appointment_date', validators=[
                    IsFutureDateValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if parse_date(value) <= datetime.now():
            raise ValidationError(
                self.error_message or f"Date '{value}' is not in the future."
            )

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
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
        value_date = self.__parse_date(value)

        if value_date <= datetime.now():
            raise ValidationError(
                self.error_message or f"Date '{value}' is not in the future."
            )

    @staticmethod
    def __parse_date(value: Any) -> datetime:
        """
        Converts a value to a datetime object.

        Supports ISO 8601 formatted strings and datetime objects.
        """

        if isinstance(value, datetime):
            return value

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid ISO 8601 format '{value}'.")

        raise ValidationError(
            f"Unsupported type for past date validation '{type(value)}'."
        )

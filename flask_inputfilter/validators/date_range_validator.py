from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional, Union

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


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
            def __init__(self):
                super().__init__()

                self.add('booking_date', validators=[
                    DateRangeValidator(
                        min_date="2023-01-01",
                        max_date="2023-01-31"
                    )
                ])
    """

    __slots__ = ("min_date", "max_date", "error_message")

    def __init__(
        self,
        min_date: Optional[Union[str, date, datetime]] = None,
        max_date: Optional[Union[str, date, datetime]] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.min_date = min_date
        self.max_date = max_date
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_date = self.__parse_date(value)
        min_date = self.__parse_date(self.min_date) if self.min_date else None
        max_date = self.__parse_date(self.max_date) if self.max_date else None

        if (min_date and value_date < min_date) or (
            max_date and value_date > max_date
        ):
            raise ValidationError(
                self.error_message
                or f"Date '{value}' is not in the range from "
                f"'{self.min_date}' to '{self.max_date}'."
            )

    @staticmethod
    def __parse_date(value: Any) -> datetime:
        """
        Converts a value to a datetime object.

        Supports ISO 8601 formatted strings and datetime objects.
        """

        if isinstance(value, datetime):
            return value

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid ISO 8601 format '{value}'.")

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        raise ValidationError(
            f"Unsupported type for past date validation '{type(value)}'."
        )

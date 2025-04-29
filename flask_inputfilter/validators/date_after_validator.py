from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional, Union

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


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
            def __init__(self):
                super().__init__()

                self.add('event_date', validators=[
                    DateAfterValidator(reference_date="2023-01-01")
                ])
    """

    __slots__ = ("reference_date", "error_message")

    def __init__(
        self,
        reference_date: Union[str, date, datetime],
        error_message: Optional[str] = None,
    ) -> None:
        self.reference_date = reference_date
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_reference_date = self.__parse_date(self.reference_date)
        value_datetime = self.__parse_date(value)

        if value_datetime < value_reference_date:
            raise ValidationError(
                self.error_message
                or f"Date '{value}' is not after '{value_reference_date}'."
            )

    @staticmethod
    def __parse_date(value: Any) -> datetime:
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
            f"Unsupported type for date comparison '{type(value)}'."
        )

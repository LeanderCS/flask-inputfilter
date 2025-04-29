from __future__ import annotations

from datetime import date
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsDateValidator(BaseValidator):
    """
    Checks if the provided value is a date object.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
        value is not a date.

    **Expected Behavior:**

    Raises a ``ValidationError`` if the input value is not of type date.

    **Example Usage:**

    .. code-block:: python

        class DateInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('event_date', validators=[
                    IsDateValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, date):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not an date."
            )

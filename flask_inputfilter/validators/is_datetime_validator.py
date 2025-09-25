from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsDateTimeValidator(BaseValidator):
    """
    Checks if the provided value is a datetime object.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a datetime.

    **Expected Behavior:**

    Raises a ``ValidationError`` if the input value is not of type datetime.

    **Example Usage:**

    .. code-block:: python

        class TimestampInputFilter(InputFilter):
            timestamp: datetime = field(validators=[
                IsDateTimeValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, datetime):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not an datetime."
            )

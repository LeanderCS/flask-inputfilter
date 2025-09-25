from __future__ import annotations

import uuid
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsUUIDValidator(BaseValidator):
    """
    Checks if the provided value is a valid UUID string.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      input is not a valid UUID.

    **Expected Behavior:**

    Verifies that the input is a string and attempts to parse it as a
    UUID. Raises a ``ValidationError`` if parsing fails.

    **Example Usage:**

    .. code-block:: python

        class UUIDInputFilter(InputFilter):
            uuid: str = field(validators=[
                IsUUIDValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        try:
            uuid.UUID(value)

        except ValueError:
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a valid UUID."
            )

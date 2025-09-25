from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsStringValidator(BaseValidator):
    """
    Validates that the provided value is a string.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a string.

    **Expected Behavior:**

    Raises a ``ValidationError`` if the input is not of type str.

    **Example Usage:**

    .. code-block:: python

        class TextInputFilter(InputFilter):
            text: str = field(validators=[
                IsStringValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a string."
            )

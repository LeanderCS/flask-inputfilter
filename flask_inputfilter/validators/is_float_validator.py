from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsFloatValidator(BaseValidator):
    """
    Checks if the provided value is a float.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a float.

    **Expected Behavior:**

    Raises a ``ValidationError`` if the input value is not of type float.

    **Example Usage:**

    .. code-block:: python

        class MeasurementInputFilter(InputFilter):
            temperature: float = field(validators=[
                IsFloatValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, float):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a float."
            )

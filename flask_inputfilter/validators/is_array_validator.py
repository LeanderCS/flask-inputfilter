from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsArrayValidator(BaseValidator):
    """
    Checks if the provided value is an array (i.e. a list).

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if
      validation fails.

    **Expected Behavior:**

    Raises a ``ValidationError`` if the input is not a list.

    **Example Usage:**

    .. code-block:: python

        class ListInputFilter(InputFilter):
            items: list = field(validators=[
                IsArrayValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, list):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not an array."
            )

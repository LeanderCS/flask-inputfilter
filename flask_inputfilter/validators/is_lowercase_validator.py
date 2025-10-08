from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsLowercaseValidator(BaseValidator):
    """
    Checks if a value is entirely lowercase. The validator ensures that the
    input string has no uppercase characters.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      value is not entirely lowercase.

    **Expected Behavior:**

    Confirms that the input is a string and verifies that all characters
    are lowercase using the string method ``islower()``. Raises a
    ``ValidationError`` if the check fails.

    **Example Usage:**

    .. code-block:: python

        class LowercaseInputFilter(InputFilter):
            username: str = field(validators=[
                IsLowercaseValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value is not entirely lowercase."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not value.islower():
            raise ValidationError(self.error_message)

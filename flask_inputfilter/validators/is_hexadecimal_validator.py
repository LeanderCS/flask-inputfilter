from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsHexadecimalValidator(BaseValidator):
    """
    Checks if a given value is a valid hexadecimal string. The input must be a
    string that can be converted to an integer using base 16.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a valid hexadecimal string.

    **Expected Behavior:**

    Verifies that the input is a string and attempts to convert it to an
    integer using base 16. Raises a ``ValidationError`` if the conversion
    fails.

    **Example Usage:**

    .. code-block:: python

        class HexInputFilter(InputFilter):
            hex_value: str = field(validators=[
                IsHexadecimalValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(
        self,
        error_message: Optional[str] = None,
    ) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        try:
            int(value, 16)

        except ValueError:
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not a valid hexadecimal string."
            )

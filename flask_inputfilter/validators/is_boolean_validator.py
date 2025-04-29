from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsBooleanValidator(BaseValidator):
    """
    Checks if the provided value is a boolean.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
        input is not a bool.

    **Expected Behavior:**

    Raises a ``ValidationError`` if the input value is not of type bool.

    **Example Usage:**

    .. code-block:: python

        class FlagInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('is_active', validators=[
                    IsBooleanValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, bool):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a boolean."
            )

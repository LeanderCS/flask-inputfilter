from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsIntegerValidator(BaseValidator):
    """
    Checks whether the provided value is an integer.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if
        the value is not an integer.

    **Expected Behavior:**

    Raises a ``ValidationError`` if the input value is not of type int.

    **Example Usage:**

    .. code-block:: python

        class NumberInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('number', validators=[
                    IsIntegerValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, int):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not an integer."
            )

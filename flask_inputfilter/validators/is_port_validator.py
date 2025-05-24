from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsPortValidator(BaseValidator):
    """
    Checks if a value is a valid network port. Valid port numbers range from 1
    to 65535.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the value
        is not a valid port number.

    **Expected Behavior:**

    Ensures that the input is an integer and that it lies within the valid
    range for port numbers. Raises a ``ValidationError`` if the value is
    outside this range.

    **Example Usage:**

    .. code-block:: python

        class PortInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('port', validators=[
                    IsPortValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value is not a valid port number."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, int):
            raise ValidationError("Value must be an integer.")

        if not (1 <= value <= 65535):
            raise ValidationError(self.error_message)

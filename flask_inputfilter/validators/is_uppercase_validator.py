from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsUppercaseValidator(BaseValidator):
    """
    Checks if a value is entirely uppercase. It verifies that the input string
    has no lowercase characters.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
        value is not entirely uppercase.

    **Expected Behavior:**

    Ensures that the input is a string and that all characters are uppercase
    using the string method ``isupper()``. Raises a ``ValidationError``
    if the check fails.

    **Example Usage:**

    .. code-block:: python

        class UppercaseInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('code', validators=[
                    IsUppercaseValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value is not entirely uppercase."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not value.isupper():
            raise ValidationError(self.error_message)

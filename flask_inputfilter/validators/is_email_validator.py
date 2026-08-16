from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator

EMAIL_PATTERN = re.compile(RegexEnum.EMAIL.value)


class IsEmailValidator(BaseValidator):
    """
    Checks if a value is a valid email address.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a valid email address.

    **Expected Behavior:**

    Ensures the input is a string and matches a regular expression pattern
    for email addresses. Raises a ``ValidationError`` if the value does not
    conform to the expected email format.

    **Example Usage:**

    .. code-block:: python

        class RegistrationInputFilter(InputFilter):
            email: str = field(validators=[
                IsEmailValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value is not a valid email address."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not EMAIL_PATTERN.match(value):
            raise ValidationError(self.error_message)

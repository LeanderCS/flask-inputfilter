from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator

PHONE_NUMBER_PATTERN = re.compile(RegexEnum.PHONE_NUMBER.value)


class IsPhoneValidator(BaseValidator):
    """
    Checks if a value is a valid phone number. Accepts international numbers
    with an optional leading ``+`` as well as common separators such as spaces,
    hyphens and parentheses.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a valid phone number.

    **Expected Behavior:**

    Ensures the input is a string and matches a regular expression pattern
    for phone numbers. Raises a ``ValidationError`` if the value does not
    conform to the expected phone number format.

    **Example Usage:**

    .. code-block:: python

        class ContactInputFilter(InputFilter):
            phone: str = field(validators=[
                IsPhoneValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value is not a valid phone number."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not PHONE_NUMBER_PATTERN.match(value):
            raise ValidationError(self.error_message)

from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator

MAC_ADDRESS_PATTERN = re.compile(RegexEnum.MAC_ADDRESS.value)


class IsMacAddressValidator(BaseValidator):
    """
    Checks if a value is a valid MAC address. It verifies common MAC address
    formats, such as colon-separated or hyphen-separated pairs of hexadecimal
    digits.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a valid MAC address.

    **Expected Behavior:**

    Ensures the input is a string and matches a regular expression pattern
    for MAC addresses. Raises a ``ValidationError`` if the value does not
    conform to the expected MAC address format.

    **Example Usage:**

    .. code-block:: python

        class NetworkInputFilter(InputFilter):
            mac_address = field(validators=[
                IsMacAddressValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value is not a valid MAC address."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not MAC_ADDRESS_PATTERN.match(value):
            raise ValidationError(self.error_message)

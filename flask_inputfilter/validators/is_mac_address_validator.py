from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator

MAC_ADDRESS_PATTERN = re.compile(RegexEnum.MAC_ADDRESS.value)


class IsMacAddressValidator(BaseValidator):
    """
    Validator that checks if a value is a valid MAC address.
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

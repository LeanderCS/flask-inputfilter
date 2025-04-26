from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsPortValidator(BaseValidator):
    """
    Validator that checks if a value is a valid network port (1-65535).
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

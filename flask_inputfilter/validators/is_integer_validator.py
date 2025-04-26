from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsIntegerValidator(BaseValidator):
    """
    Validator that checks if a value is an integer.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, int):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not an integer."
            )

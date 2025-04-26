from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsFloatValidator(BaseValidator):
    """
    Validator that checks if a value is a float.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, float):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a float."
            )

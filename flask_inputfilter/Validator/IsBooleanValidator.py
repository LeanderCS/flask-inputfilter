from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsBooleanValidator(BaseValidator):
    """
    Validator that checks if a value is a bool.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, bool):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a boolean."
            )

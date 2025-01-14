from typing import Any, Optional

from ..Exception import ValidationError
from .BaseValidator import BaseValidator


class IsStringValidator(BaseValidator):
    """
    Validator that checks if a value is a string.
    """

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a string."
            )

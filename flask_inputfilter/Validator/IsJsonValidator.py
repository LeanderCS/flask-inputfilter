import json
from typing import Any, Optional

from ..Exception import ValidationError
from .BaseValidator import BaseValidator


class IsJsonValidator(BaseValidator):
    """
    Validator that checks if a value is a valid JSON string.
    """

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        try:
            json.loads(value)

        except (TypeError, ValueError):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not a valid JSON string."
            )

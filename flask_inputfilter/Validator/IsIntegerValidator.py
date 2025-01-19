from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsIntegerValidator(BaseValidator):
    """
    Validator that checks if a value is an integer.
    """

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, int):
            raise ValidationError(
                self.error_message, f"Value '{value}' is not an integer."
            )

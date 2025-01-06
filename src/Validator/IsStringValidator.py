from typing import Any

from ..Exception.ValidationError import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsStringValidator(BaseValidator):
    """
    Validator that checks if a value is a string.
    """

    def validate(self, value: Any) -> None:

        if not isinstance(value, str):
            raise ValidationError(f"Value '{value}' is not a string.")

from typing import Any

from ..Exception.ValidationError import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsIntegerValidator(BaseValidator):
    """
    Validator that checks if a value is an integer.
    """

    def validate(self, value: Any) -> None:

        if not isinstance(value, int):
            raise ValidationError(f"Value '{value}' is not an integer.")

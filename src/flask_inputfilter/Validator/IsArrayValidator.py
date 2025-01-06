from typing import Any

from ..Exception import ValidationError
from ..Validator import BaseValidator


class IsArrayValidator(BaseValidator):
    """
    Validator that checks if a value is an array.
    """

    def validate(self, value: Any) -> None:

        if not isinstance(value, list):
            raise ValidationError(f"Value '{value}' is not an array.")

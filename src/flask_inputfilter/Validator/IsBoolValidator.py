from typing import Any

from ..Exception import ValidationError
from ..Validator import BaseValidator


class IsBoolValidator(BaseValidator):
    """
    Validator that checks if a value is a bool.
    """

    def validate(self, value: Any) -> None:

        if not isinstance(value, bool):
            raise ValidationError(f"Value '{value}' is not a bool.")

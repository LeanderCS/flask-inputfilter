from typing import Any

from src.flask_inputfilter.Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsIntegerValidator(BaseValidator):
    """
    Validator that checks if a value is an integer.
    """

    def validate(self, value: Any) -> None:

        if not isinstance(value, int):
            raise ValidationError(f"Value '{value}' is not an integer.")

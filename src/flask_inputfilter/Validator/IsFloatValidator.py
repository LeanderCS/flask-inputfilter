from typing import Any
from src.flask_inputfilter.Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsFloatValidator(BaseValidator):
    """
    Validator that checks if a value is a float.
    """

    def validate(self, value: Any) -> None:

        if not isinstance(value, float):
            raise ValidationError(f"Value '{value}' is not a float.")

from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator.BaseValidator import BaseValidator


class ArrayLengthValidator(BaseValidator):
    """
    Validator that checks if the length of an array is within
    the specified range.
    """

    def __init__(
        self,
        min_length: int = 0,
        max_length: int = float("inf"),
        error_message: Optional[str] = None,
    ) -> None:
        self.min_length = min_length
        self.max_length = max_length
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, list):
            raise ValidationError(f"Value '{value}' must be a list.")

        array_length = len(value)

        if not (self.min_length <= array_length <= self.max_length):
            raise ValidationError(
                self.error_message
                or f"Array length must be between '{self.min_length}' "
                f"and '{self.max_length}'."
            )

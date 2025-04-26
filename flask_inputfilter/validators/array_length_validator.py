from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class ArrayLengthValidator(BaseValidator):
    """
    Validator that checks if the length of an array is within
    the specified range.
    """

    __slots__ = ("min_length", "max_length", "error_message")

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

        if not (self.min_length <= len(value) <= self.max_length):
            raise ValidationError(
                self.error_message
                or f"Array length must be between '{self.min_length}' "
                f"and '{self.max_length}'."
            )

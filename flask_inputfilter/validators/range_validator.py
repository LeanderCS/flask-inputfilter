from __future__ import annotations

from typing import Any, Optional, Union

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class RangeValidator(BaseValidator):
    """
    Validator that checks if a numeric value is within a specified range.
    """

    __slots__ = ("min_value", "max_value", "error_message")

    def __init__(
        self,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, (int, float)):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a number."
            )

        if (self.min_value is not None and value < self.min_value) or (
            self.max_value is not None and value > self.max_value
        ):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not within the range of "
                f"'{self.min_value}' to '{self.max_value}'."
            )

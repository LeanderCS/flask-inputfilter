from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class RangeValidator(BaseValidator):
    """
    Validator that checks if a numeric value is within a specified range.
    """

    def __init__(
        self,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if (self.min_value is not None and value < self.min_value) or (
            self.max_value is not None and value > self.max_value
        ):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not within the range of "
                f"'{self.min_value}' to '{self.max_value}'."
            )

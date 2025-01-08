from typing import Any

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class RangeValidator(BaseValidator):
    """
    Validator that checks if a numeric value is within a specified range.
    """

    def __init__(
        self,
        min_value: float = None,
        max_value: float = None,
        error_message: str = "Value '{}' is not within the range {} to {}.",
    ) -> None:

        self.min_value = min_value
        self.max_value = max_value
        self.error_message = error_message

    def validate(self, value: Any) -> None:

        if (self.min_value is not None and value < self.min_value) or (
            self.max_value is not None and value > self.max_value
        ):
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(
                        value, self.min_value, self.max_value
                    )
                )

            raise ValidationError(self.error_message)

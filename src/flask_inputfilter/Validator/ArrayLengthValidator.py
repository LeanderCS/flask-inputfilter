from typing import Any

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class ArrayLengthValidator(BaseValidator):
    """
    Validator that checks if the length of an array is within the specified range.
    """

    def __init__(
        self,
        min_length: int = 0,
        max_length: int = float("inf"),
        error_message: str = "Array length must be between {} and {}.",
    ) -> None:

        self.min_length = min_length
        self.max_length = max_length
        self.error_message = error_message

    def validate(self, value: Any) -> None:

        if not isinstance(value, list):
            raise ValidationError("Value must be a list.")

        array_length = len(value)

        if not (self.min_length <= array_length <= self.max_length):
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(self.min_length, self.max_length)
                )

            raise ValidationError(self.error_message)

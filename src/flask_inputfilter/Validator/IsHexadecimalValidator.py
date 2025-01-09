from typing import Any

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsHexadecimalValidator(BaseValidator):
    """
    Validator that checks if a value is a valid hexadecimal string.
    """

    def __init__(
        self,
        error_message: str = "Value '{}' is not a valid hexadecimal string.",
    ) -> None:

        self.error_message = error_message

    def validate(self, value: Any) -> None:

        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        try:
            int(value, 16)

        except ValueError:
            raise ValidationError(self.error_message.format(value))

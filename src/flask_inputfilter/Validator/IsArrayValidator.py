from typing import Any

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsArrayValidator(BaseValidator):
    """
    Validator that checks if a value is an array.
    """

    def __init__(
        self, error_message: str = "Value '{}' is not an array."
    ) -> None:

        self.error_message = error_message

    def validate(self, value: Any) -> None:

        if not isinstance(value, list):
            if "{}" in self.error_message:
                raise ValidationError(self.error_message.format(value))

            raise ValidationError(self.error_message)

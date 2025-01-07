import json
from typing import Any

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsJsonValidator(BaseValidator):
    """
    Validator that checks if a value is a valid JSON string.
    """

    def __init__(
        self, error_message: str = "Value '{}' is not a valid JSON string."
    ) -> None:

        self.error_message = error_message

    def validate(self, value: Any) -> None:

        try:
            json.loads(value)

        except (TypeError, ValueError):
            if "{}" in self.error_message:
                raise ValidationError(self.error_message.format(value))

            raise ValidationError(self.error_message)

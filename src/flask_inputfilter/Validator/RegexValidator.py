import re

from ..Exception import ValidationError
from ..Validator import BaseValidator


class RegexValidator(BaseValidator):
    """
    Validator that checks if a value matches a given regular
    expression pattern.
    """

    def __init__(self, pattern: str, errorMessage: str = None) -> None:

        self.pattern = pattern
        self.errorMessage = errorMessage

    def validate(self, value: str) -> None:

        if not re.match(self.pattern, value):
            if self.errorMessage:
                raise ValidationError(self.errorMessage)

            raise ValidationError(
                f"Value '{value}' does not match the required pattern "
                f"'{self.pattern}'.")

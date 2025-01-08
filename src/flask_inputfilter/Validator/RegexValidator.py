import re

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class RegexValidator(BaseValidator):
    """
    Validator that checks if a value matches a given regular
    expression pattern.
    """

    def __init__(
        self,
        pattern: str,
        error_message: str = "Value '{}' does not match the required pattern '{}'.",
    ) -> None:

        self.pattern = pattern
        self.error_message = error_message

    def validate(self, value: str) -> None:

        if not re.match(self.pattern, value):
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(value, self.pattern)
                )

            raise ValidationError(self.error_message)

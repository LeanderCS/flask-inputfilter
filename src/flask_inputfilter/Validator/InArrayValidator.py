from typing import Any, List

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class InArrayValidator(BaseValidator):
    """
    Validator that checks if a value is in a given list of allowed values.
    """

    def __init__(
        self,
        haystack: List[Any],
        strict: bool = False,
        error_message: str = "Value '{}' is not in the allowed values '{}'.",
    ) -> None:

        self.haystack = haystack
        self.strict = strict
        self.error_message = error_message

    def validate(self, value: Any) -> None:

        try:
            if self.strict:
                if value not in self.haystack or not any(
                    isinstance(value, type(item)) for item in self.haystack
                ):
                    raise ValidationError

            else:
                if value not in self.haystack:
                    raise ValidationError

        except Exception:
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(value, self.haystack)
                )

            raise ValidationError(self.error_message)

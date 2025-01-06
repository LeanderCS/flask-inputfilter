from typing import Any, List

from ..Exception import ValidationError
from ..Validator import BaseValidator


class InArrayValidator(BaseValidator):
    """
    Validator that checks if a value is in a given list of allowed values.
    """

    def __init__(self, haystack: List[Any], strict: bool = False) -> None:

        self.haystack = haystack
        self.strict = strict

    def validate(self, value: Any) -> None:

        if self.strict and value not in self.haystack:
            raise ValidationError(
                f"Value '{value}' is not in the allowed values.")

        elif value not in self.haystack:
            raise ValidationError(
                f"Value '{value}' is not in the allowed values"
                f"(non-strict check).")

from __future__ import annotations

from typing import Any, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class NotInArrayValidator(BaseValidator):
    """
    Validator that checks if a value is in a given list of disallowed values.
    """

    __slots__ = ("haystack", "strict", "error_message")

    def __init__(
        self,
        haystack: List[Any],
        strict: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        self.haystack = haystack
        self.strict = strict
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        is_disallowed = value in self.haystack
        is_type_mismatch = self.strict and not any(
            isinstance(value, type(item)) for item in self.haystack
        )

        if is_disallowed or is_type_mismatch:
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is in the disallowed values "
                f"'{self.haystack}'."
            )

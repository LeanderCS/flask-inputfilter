from __future__ import annotations

from typing import Any, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class InArrayValidator(BaseValidator):
    """
    Validator that checks if a value is in a given list of allowed values.
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
        try:
            if self.strict:
                if value not in self.haystack or not any(
                    isinstance(value, type(item)) for item in self.haystack
                ):
                    raise ValidationError

            else:
                if value not in self.haystack:
                    raise ValidationError

        except ValidationError:
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not in the allowed "
                f"values '{self.haystack}'."
            )

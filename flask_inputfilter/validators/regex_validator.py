from __future__ import annotations

import re
from typing import Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class RegexValidator(BaseValidator):
    """
    Validator that checks if a value matches a given regular
    expression pattern.
    """

    __slots__ = ("pattern", "error_message")

    def __init__(
        self,
        pattern: str,
        error_message: Optional[str] = None,
    ) -> None:
        self.pattern = pattern
        self.error_message = error_message

    def validate(self, value: str) -> None:
        if not re.match(self.pattern, value):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' does not match the required "
                f"pattern '{self.pattern}'."
            )

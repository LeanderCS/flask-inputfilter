from __future__ import annotations

import json
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsJsonValidator(BaseValidator):
    """
    Validator that checks if a value is a valid JSON string.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        try:
            json.loads(value)

        except (TypeError, ValueError):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not a valid JSON string."
            )

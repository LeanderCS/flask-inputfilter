from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsDateTimeValidator(BaseValidator):
    """
    Validator that checks if a value is a date.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, datetime):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not an datetime."
            )

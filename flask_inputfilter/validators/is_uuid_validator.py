from __future__ import annotations

import uuid
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsUUIDValidator(BaseValidator):
    """
    Validator that checks if a value is a valid UUID string.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        try:
            uuid.UUID(value)

        except ValueError:
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a valid UUID."
            )

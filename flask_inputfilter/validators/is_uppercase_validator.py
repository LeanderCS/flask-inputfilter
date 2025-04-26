from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsUppercaseValidator(BaseValidator):
    """
    Validator that checks if a value is entirely uppercase.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value is not entirely uppercase."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not value.isupper():
            raise ValidationError(self.error_message)

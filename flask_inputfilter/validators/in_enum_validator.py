from __future__ import annotations

from enum import Enum
from typing import Any, Optional, Type

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class InEnumValidator(BaseValidator):
    """
    Validator that checks if a value is in a given Enum.
    """

    __slots__ = ("enumClass", "error_message")

    def __init__(
        self,
        enumClass: Type[Enum],
        error_message: Optional[str] = None,
    ) -> None:
        self.enumClass = enumClass
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not any(
            value.lower() == item.name.lower() for item in self.enumClass
        ):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not an value of '{self.enumClass}'"
            )

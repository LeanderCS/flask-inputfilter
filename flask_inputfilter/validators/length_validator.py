from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class LengthEnum(Enum):
    """
    Enum that defines the possible length types.
    """

    LEAST = "least"
    MOST = "most"


class LengthValidator(BaseValidator):
    """
    Validator that checks the length of a string value.
    """

    __slots__ = ("min_length", "max_length", "error_message")

    def __init__(
        self,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.min_length = min_length
        self.max_length = max_length
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if (self.max_length is not None and len(value) < self.min_length) or (
            self.max_length is not None and len(value) > self.max_length
        ):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not within the range of "
                f"'{self.min_length}' to '{self.max_length}'."
            )

from __future__ import annotations

from typing import Any, Optional, Type

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsInstanceValidator(BaseValidator):
    """
    Validator that checks if a value is an instance of a given class.
    """

    __slots__ = ("class_type", "error_message")

    def __init__(
        self,
        classType: Type[Any],
        error_message: Optional[str] = None,
    ) -> None:
        self.class_type = classType
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, self.class_type):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not an instance "
                f"of '{self.class_type}'."
            )

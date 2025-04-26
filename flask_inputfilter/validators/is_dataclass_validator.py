from __future__ import annotations

from typing import Any, Optional, Type, TypeVar

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator

T = TypeVar("T")


class IsDataclassValidator(BaseValidator):
    """
    Validator that checks if a value is a dataclass.
    """

    __slots__ = ("dataclass_type", "error_message")

    def __init__(
        self,
        dataclass_type: Type[T],
        error_message: Optional[str] = None,
    ) -> None:
        self.dataclass_type = dataclass_type
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, dict):
            raise ValidationError(
                self.error_message
                or "The provided value is not a dict instance."
            )

        expected_keys = self.dataclass_type.__annotations__.keys()
        if any(key not in value for key in expected_keys):
            raise ValidationError(
                self.error_message
                or f"'{value}' is not an instance "
                f"of '{self.dataclass_type}'."
            )

from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsTypedDictValidator(BaseValidator):
    """
    Validator that checks if a value is a TypedDict.
    """

    __slots__ = ("typed_dict_type", "error_message")

    def __init__(
        self,
        typed_dict_type,
        error_message: Optional[str] = None,
    ) -> None:
        """
        Parameters:
            typed_dict_type (Type[TypedDict]): The TypedDict class
                to validate against.
            error_message (Optional[str]): Custom error message to
                use if validation fails.
        """

        self.typed_dict_type = typed_dict_type
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, dict):
            raise ValidationError(
                self.error_message
                or "The provided value is not a dict instance."
            )

        expected_keys = self.typed_dict_type.__annotations__
        for key, expected_type in expected_keys.items():
            if key not in value:
                raise ValidationError(
                    self.error_message
                    or f"'{value}' does not match "
                    f"'{self.typed_dict_type.__name__}' structure: "
                    f"Missing key '{key}'."
                )
            if not isinstance(value[key], expected_type):
                raise ValidationError(
                    self.error_message
                    or f"'{value}' does not match "
                    f"'{self.typed_dict_type.__name__}' structure: "
                    f"Key '{key}' has invalid type."
                )

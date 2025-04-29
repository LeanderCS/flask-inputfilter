from __future__ import annotations

from typing import Any, Optional, Type, TypeVar

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator

T = TypeVar("T")


class IsDataclassValidator(BaseValidator):
    """
    Validates that the provided value conforms to a specific dataclass type.

    **Parameters:**

    - **dataclass_type** (*Type[dict]*): The expected dataclass type.
    - **error_message** (*Optional[str]*): Custom error message if
        validation fails.

    **Expected Behavior:**

    Ensures the input is a dictionary and, that all expected keys are
    present. Raises a ``ValidationError`` if the structure does not match.

    **Example Usage:**

    .. code-block:: python

        from dataclasses import dataclass

        @dataclass
        class User:
            id: int
            name: str

        class UserInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('user', validators=[
                    IsDataclassValidator(dataclass_type=User)
                ])
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

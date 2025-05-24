from __future__ import annotations

from enum import Enum
from typing import Any, Optional, Type

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class InEnumValidator(BaseValidator):
    """
    Verifies that a given value is a valid member of a specified Enum class.

    **Parameters:**

    - **enumClass** (*Type[Enum]*): The Enum to validate against.
    - **error_message** (*Optional[str]*): Custom error message if
        validation fails.

    **Expected Behavior:**

    Performs a case-insensitive comparison to ensure that the value matches
    one of the Enum's member names. Raises a ``ValidationError`` if the value
    is not a valid Enum member.

    **Example Usage:**

    .. code-block:: python

        from enum import Enum

        class ColorEnum(Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

        class ColorInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('color', validators=[
                    InEnumValidator(enumClass=ColorEnum)
                ])
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

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Type

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator

if TYPE_CHECKING:
    from enum import Enum


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
            color: str = field(
                validators=[InEnumValidator(enum_class=ColorEnum)]
            )
    """

    __slots__ = ("enum_class", "error_message")

    def __init__(
        self,
        enum_class: Type[Enum],
        error_message: Optional[str] = None,
    ) -> None:
        self.enum_class = enum_class
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not any(
            value.lower() == item.name.lower() for item in self.enum_class
        ):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not an value of '{self.enum_class}'"
            )

from enum import Enum
from typing import Any, Type

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class InEnumValidator(BaseValidator):
    """
    Validator that checks if a value is in a given Enum.
    """

    def __init__(
        self,
        enumClass: Type[Enum],
        error_message: str = "Value '{}' is not an value of '{}'",
    ) -> None:

        self.enumClass = enumClass
        self.error_message = error_message

    def validate(self, value: Any) -> None:

        if not any(
            value.lower() == item.name.lower() for item in self.enumClass
        ):
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(value, self.enumClass)
                )

            raise ValidationError(self.error_message)

from enum import Enum
from typing import Type, Any

from ..Exception import ValidationError
from ..Validator import BaseValidator


class InEnumValidator(BaseValidator):
    """
    Validator that checks if a value is in a given Enum.
    """

    def __init__(self, enumClass: Type[Enum]) -> None:

        self.enumClass = enumClass

    def validate(self, value: Any) -> None:

        if not any(value.lower() == item.name.lower()
                   for item in self.enumClass):
            raise ValidationError(
                f"Value '{value}' is not an value of {self.enumClass}.")

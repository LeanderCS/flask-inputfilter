from enum import Enum
from typing import Any

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


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

    def __init__(
        self,
        min_length: int = 0,
        max_length: int = None,
        error_message: str = "Value '{}' must be at {} '{}' characters long.",
    ) -> None:

        self.min_length = min_length
        self.max_length = max_length
        self.error_message = error_message

    def validate(self, value: Any) -> None:

        if len(value) < self.min_length:
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(
                        value, LengthEnum.LEAST.value, self.min_length
                    )
                )

            raise ValidationError(self.error_message)

        if self.max_length is not None and len(value) > self.max_length:
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(
                        value, LengthEnum.MOST.value, self.max_length
                    )
                )

            raise ValidationError(self.error_message)

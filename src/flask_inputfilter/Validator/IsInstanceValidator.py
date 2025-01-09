from typing import Any, Type

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsInstanceValidator(BaseValidator):
    """
    Validator that checks if a value is an instance of a given class.
    """

    def __init__(
        self,
        classType: Type[Any],
        error_message: str = "Value '{}' is not an instance of '{}'.",
    ) -> None:

        self.classType = classType
        self.error_message = error_message

    def validate(self, value: Any) -> None:

        if not isinstance(value, self.classType):
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(value, self.classType)
                )

            raise ValidationError(self.error_message)

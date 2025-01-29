from dataclasses import is_dataclass
from typing import Any, Optional, Type

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsDataclassValidator(BaseValidator):
    """
    Validator that checks if a value is a dataclass.
    """

    def __init__(
        self,
        dataclass_type: Optional[Type[dict]] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.dataclass_type = dataclass_type
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not is_dataclass(value):
            raise ValidationError(
                self.error_message
                or "The provided value is not a dataclass instance."
            )

        if self.dataclass_type and not isinstance(value, self.dataclass_type):
            raise ValidationError(
                self.error_message
                or f"'{value}' is not an instance "
                f"of '{self.dataclass_type}'."
            )

from typing import Any, Optional, Type

from typing_extensions import TypedDict

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsTypedDictValidator(BaseValidator):
    """
    Validator that checks if a value is a TypedDict.
    """

    def __init__(
        self,
        typed_dict_type: Optional[Type[TypedDict]] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.typed_dict_type = typed_dict_type
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, dict):
            raise ValidationError(
                self.error_message
                or "The provided value is not a TypedDict instance."
            )

        if self.typed_dict_type:
            expected_keys = self.typed_dict_type.__annotations__.keys()
            if not all(key in value for key in expected_keys):
                raise ValidationError(
                    self.error_message
                    or f"'{value}' does not match "
                    f"{self.typed_dict_type.__name__} structure."
                )

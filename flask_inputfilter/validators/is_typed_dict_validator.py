from __future__ import annotations

from typing import Any, Optional, Type

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsTypedDictValidator(BaseValidator):
    """
    Validates that the provided value conforms to a specified TypedDict
    structure.

    **Parameters:**

    - **typed_dict_type** (*Type[TypedDict]*): The TypedDict class that
      defines the expected structure.
    - **error_message** (*Optional[str]*): Custom error message if the
      validation fails.

    **Expected Behavior:**

    Ensures the input is a dictionary and, that all expected keys are present.
    Raises a ``ValidationError`` if the structure does not match.

    **Example Usage:**

    .. code-block:: python

        from typing import TypedDict

        class PersonDict(TypedDict):
            name: str
            age: int

        class PersonInputFilter(InputFilter):
            person = field(validators=[
                IsTypedDictValidator(typed_dict_type=PersonDict)
            ])
    """

    __slots__ = (
        "error_message",
        "typed_dict_expected_keys",
        "typed_dict_name",
    )

    def __init__(
        self,
        typed_dict_type: Type,
        error_message: Optional[str] = None,
    ) -> None:
        """
        Parameters:
            typed_dict_type (Type[TypedDict]): The TypedDict class
                to validate against.
            error_message (Optional[str]): Custom error message to
                use if validation fails.
        """

        self.typed_dict_expected_keys = typed_dict_type.__annotations__
        self.typed_dict_name = typed_dict_type.__name__
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, dict):
            raise ValidationError(
                self.error_message
                or "The provided value is not a dict instance."
            )

        for key, expected_type in self.typed_dict_expected_keys.items():
            if key not in value:
                raise ValidationError(
                    self.error_message
                    or f"'{value}' does not match "
                    f"'{self.typed_dict_name}' structure: "
                    f"Missing key '{key}'."
                )
            if not isinstance(value[key], expected_type):
                raise ValidationError(
                    self.error_message
                    or f"'{value}' does not match "
                    f"'{self.typed_dict_name}' structure: "
                    f"Key '{key}' has invalid type."
                )

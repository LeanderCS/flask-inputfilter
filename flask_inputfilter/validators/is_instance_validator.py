from __future__ import annotations

from typing import Any, Optional, Type

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsInstanceValidator(BaseValidator):
    """
    Validates that the provided value is an instance of a specified class.

    **Parameters:**

    - **classType** (*Type[Any]*): The class against which the value is
        validated.
    - **error_message** (*Optional[str]*): Custom error message if the
        validation fails.

    **Expected Behavior:**

    Raises a ``ValidationError`` if the input is not an instance of the
    specified class.

    **Example Usage:**

    .. code-block:: python

        class MyClass:
            pass

        class InstanceInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('object', validators=[
                    IsInstanceValidator(classType=MyClass)
                ])
    """

    __slots__ = ("class_type", "error_message")

    def __init__(
        self,
        classType: Type[Any],
        error_message: Optional[str] = None,
    ) -> None:
        self.class_type = classType
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, self.class_type):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not an instance "
                f"of '{self.class_type}'."
            )

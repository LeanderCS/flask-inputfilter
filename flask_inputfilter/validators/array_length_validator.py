from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class ArrayLengthValidator(BaseValidator):
    """
    Checks whether the length of an array falls within a specified range.

    **Parameters:**

    - **min_length** (*int*, default: 0): The minimum number of
        elements required.
    - **max_length** (*int*, default: infinity): The maximum number
        of allowed elements.
    - **error_message** (*Optional[str]*): Custom error message if the
        length check fails.

    **Expected Behavior:**

    Ensures that the input is a list and that its length is between the
    specified minimum and maximum. If not, a ``ValidationError`` is raised.

    **Example Usage:**

    .. code-block:: python

        class ListInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('items', validators=[
                    ArrayLengthValidator(min_length=1, max_length=5)
                ])
    """

    __slots__ = ("min_length", "max_length", "error_message")

    def __init__(
        self,
        min_length: int = 0,
        max_length: int = float("inf"),
        error_message: Optional[str] = None,
    ) -> None:
        self.min_length = min_length
        self.max_length = max_length
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, list):
            raise ValidationError(f"Value '{value}' must be a list.")

        if not (self.min_length <= len(value) <= self.max_length):
            raise ValidationError(
                self.error_message
                or f"Array length must be between '{self.min_length}' "
                f"and '{self.max_length}'."
            )

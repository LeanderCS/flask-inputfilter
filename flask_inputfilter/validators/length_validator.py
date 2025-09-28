from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class LengthValidator(BaseValidator):
    """
    Validates the length of a string, ensuring it falls within a specified
    range.

    **Parameters:**

    - **min_length** (*Optional[int]*): The minimum allowed length.
    - **max_length** (*Optional[int]*): The maximum allowed length.
    - **error_message** (*Optional[str]*): Custom error message if
      the validation fails.

    **Expected Behavior:**

    Checks the length of the input string and raises a ``ValidationError``
    if it is shorter than ``min_length`` or longer than ``max_length``.

    **Example Usage:**

    .. code-block:: python

        class TextLengthInputFilter(InputFilter):
            username: str = field(validators=[
                LengthValidator(min_length=3, max_length=15)
            ])
    """

    __slots__ = ("error_message", "max_length", "min_length")

    def __init__(
        self,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.min_length = min_length
        self.max_length = max_length
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if (self.min_length is not None and len(value) < self.min_length) or (
            self.max_length is not None and len(value) > self.max_length
        ):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not within the range of "
                f"'{self.min_length}' to '{self.max_length}'."
            )

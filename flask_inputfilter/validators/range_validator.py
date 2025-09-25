from __future__ import annotations

from typing import Any, Optional, Union

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class RangeValidator(BaseValidator):
    """
    Checks whether a numeric value falls within a specified range.

    **Parameters:**

    - **min_value** (*Optional[float]*): The minimum allowed value.
    - **max_value** (*Optional[float]*): The maximum allowed value.
    - **error_message** (*Optional[str]*): Custom error message if the
      validation fails.

    **Expected Behavior:**

    Verifies that the numeric input is not less than ``min_value`` and
    not greater than ``max_value``. Raises a ``ValidationError`` if the
    value is outside this range.

    **Example Usage:**

    .. code-block:: python

        class ScoreInputFilter(InputFilter):
            score: float = field(validators=[
                RangeValidator(min_value=0, max_value=100)
            ])
    """

    __slots__ = ("error_message", "max_value", "min_value")

    def __init__(
        self,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, (int, float)):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not a number."
            )

        if (self.min_value is not None and value < self.min_value) or (
            self.max_value is not None and value > self.max_value
        ):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not within the range of "
                f"'{self.min_value}' to '{self.max_value}'."
            )

from __future__ import annotations

import json
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsJsonValidator(BaseValidator):
    """
    Validates that the provided value is a valid JSON string.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if
      the input is not a valid JSON string.

    **Expected Behavior:**

    Attempts to parse the input using JSON decoding. Raises a
    ``ValidationError`` if parsing fails.

    **Example Usage:**

    .. code-block:: python

        class JsonInputFilter(InputFilter):
            json_data: str = field(validators=[
                IsJsonValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        try:
            json.loads(value)

        except (TypeError, ValueError):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not a valid JSON string."
            )

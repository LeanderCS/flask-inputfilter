from __future__ import annotations

import re
from typing import Optional, Union

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class RegexValidator(BaseValidator):
    """
    Validates that the input string matches a specified regular expression
    pattern.

    **Parameters:**

    - **pattern** (*str | RegexEnum*): The regular expression pattern or
      value of RegexEnum the input must match.
    - **error_message** (*Optional[str]*): Custom error message if
      the input does not match the pattern.

    **Expected Behavior:**

    Uses the Python ``re`` module to compare the input string against
    the provided pattern. Raises a ``ValidationError`` if there is no match.

    **Example Usage:**

    .. code-block:: python

        class EmailInputFilter(InputFilter):
            email: str = field(validators=[
                RegexValidator(pattern=r'[a-cA-C]+')
            ])
    """

    __slots__ = ("_compiled_pattern", "error_message", "pattern")

    def __init__(
        self,
        pattern: Union[str, RegexEnum],
        error_message: Optional[str] = None,
    ) -> None:
        self.pattern = (
            pattern.value if isinstance(pattern, RegexEnum) else pattern
        )
        self._compiled_pattern = re.compile(self.pattern)
        self.error_message = error_message

    def validate(self, value: str) -> None:
        if not self._compiled_pattern.match(value):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' does not match the required "
                f"pattern '{self.pattern}'."
            )

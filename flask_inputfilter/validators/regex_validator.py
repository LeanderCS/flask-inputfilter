from __future__ import annotations

import re
from typing import ClassVar, Optional, Pattern

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator
from flask_inputfilter.performance_config import PerformanceConfig


class RegexValidator(BaseValidator):
    """
    Validates that the input string matches a specified regular expression
    pattern.

    **Parameters:**

    - **pattern** (*str*): The regular expression pattern the
      input must match.
    - **error_message** (*Optional[str]*): Custom error message if
      the input does not match the pattern.

    **Expected Behavior:**

    Uses the Python ``re`` module to compare the input string against
    the provided pattern. Raises a ``ValidationError`` if there is no match.

    **Example Usage:**

    .. code-block:: python

        class EmailInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('email', validators=[
                    RegexValidator(pattern=r'[a-cA-C]+')
                ])
    """

    __slots__ = ("_compiled_pattern", "error_message", "pattern")
    _pattern_cache: ClassVar[dict[str, Pattern]] = {}

    def __init__(
        self,
        pattern: str,
        error_message: Optional[str] = None,
    ) -> None:
        self.pattern = pattern
        self.error_message = error_message
        if pattern not in self._pattern_cache:
            if len(self._pattern_cache) >= PerformanceConfig.REGEX_CACHE_SIZE:
                self._pattern_cache.pop(next(iter(self._pattern_cache)))
            self._pattern_cache[pattern] = re.compile(pattern)
        self._compiled_pattern = self._pattern_cache[pattern]

    def validate(self, value: str) -> None:
        if not self._compiled_pattern.match(value):
            raise ValidationError(
                self.error_message
                or f"Value '{value}' does not match the required "
                f"pattern '{self.pattern}'."
            )

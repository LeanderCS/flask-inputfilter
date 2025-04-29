from __future__ import annotations

from typing import Any, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class NotInArrayValidator(BaseValidator):
    """
    Ensures that the provided value is not present in a specified list of
    disallowed values.

    **Parameters:**

    - **haystack** (*List[Any]*): A list of disallowed values.
    - **strict** (*bool*, default: False): If ``True``, the type of the
        value is also validated against the disallowed list.
    - **error_message** (*Optional[str]*): Custom error message if the
        validation fails.

    **Expected Behavior:**

    Raises a ``ValidationError`` if the value is found in the disallowed list,
    or if strict type checking is enabled and the value's type does not match
    any allowed type.

    **Example Usage:**

    .. code-block:: python

        class UsernameInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('username', validators=[
                    NotInArrayValidator(haystack=["admin", "root"])
                ])
    """

    __slots__ = ("haystack", "strict", "error_message")

    def __init__(
        self,
        haystack: List[Any],
        strict: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        self.haystack = haystack
        self.strict = strict
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        is_disallowed = value in self.haystack
        is_type_mismatch = self.strict and not any(
            isinstance(value, type(item)) for item in self.haystack
        )

        if is_disallowed or is_type_mismatch:
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is in the disallowed values "
                f"'{self.haystack}'."
            )

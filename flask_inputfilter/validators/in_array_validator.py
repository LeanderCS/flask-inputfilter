from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class InArrayValidator(BaseValidator):
    """
    Checks that the provided value exists within a predefined list of allowed
    values.

    **Parameters:**

    - **haystack** (*list[Any]*): The list of allowed values.
    - **strict** (*bool*, default: False): When ``True``, also checks that
      the type of the value matches the types in the allowed list.
    - **error_message** (*Optional[str]*): Custom error message if
      validation fails.

    **Expected Behavior:**

    Verifies that the value is present in the list. In strict mode, type
    compatibility is also enforced. If the check fails, a ``ValidationError``
    is raised.

    **Example Usage:**

    .. code-block:: python

        class StatusInputFilter(InputFilter):
            status: str = field(validators=[
                InArrayValidator(haystack=["active", "inactive"])
            ])
    """

    __slots__ = ("error_message", "haystack", "strict")

    def __init__(
        self,
        haystack: list[Any],
        strict: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        self.haystack = haystack
        self.strict = strict
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        try:
            if self.strict:
                if value not in self.haystack or not any(
                    isinstance(value, type(item)) for item in self.haystack
                ):
                    raise ValidationError

            else:
                if value not in self.haystack:
                    raise ValidationError

        except ValidationError:
            raise ValidationError(
                self.error_message
                or f"Value '{value}' is not in the allowed "
                f"values '{self.haystack}'."
            )

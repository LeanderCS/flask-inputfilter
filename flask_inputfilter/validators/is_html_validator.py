from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsHtmlValidator(BaseValidator):
    """
    Checks if a value contains valid HTML. The validator looks for the presence
    of HTML tags in the input string.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the value
      does not contain valid HTML.

    **Expected Behavior:**

    Verifies that the input is a string and checks for HTML tags using a
    regular expression. Raises a ``ValidationError`` if no HTML tags are found.

    **Example Usage:**

    .. code-block:: python

        class HtmlInputFilter(InputFilter):
            html_content: str = field(validators=[
                IsHtmlValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value does not contain valid HTML."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not re.search(r"<\s*\w+[^>]*", value):
            raise ValidationError(self.error_message)

from __future__ import annotations

import urllib
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsUrlValidator(BaseValidator):
    """
    Checks if a value is a valid URL. The validator uses URL parsing to ensure
    that the input string contains a valid scheme and network location.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
        value is not a valid URL.

    **Expected Behavior:**

    Verifies that the input is a string and uses URL parsing
    (via ``urllib.parse.urlparse``) to confirm that both the scheme and
    network location are present. Raises a ``ValidationError`` if the URL
    is invalid.

    **Example Usage:**

    .. code-block:: python

        class UrlInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('website', validators=[
                    IsUrlValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message or "Value is not a valid URL."

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        parsed = urllib.parse.urlparse(value)

        if not (parsed.scheme and parsed.netloc):
            raise ValidationError(self.error_message)

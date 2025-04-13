from __future__ import annotations

import urllib
from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsUrlValidator(BaseValidator):
    """
    Validator that checks if a value is a valid URL.
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

from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsHtmlValidator(BaseValidator):
    """
    Validator that checks if a value contains valid HTML.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value does not contain valid HTML."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not re.search(r"<\s*\w+.*?>", value):
            raise ValidationError(self.error_message)

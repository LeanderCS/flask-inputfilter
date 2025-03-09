import re
from typing import Any, Optional

from flask_inputfilter.Enum import RegexEnum
from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator

MIME_TYPE_PATTERN = re.compile(RegexEnum.MIME_TYPE.value, re.IGNORECASE)


class IsMimeTypeValidator(BaseValidator):
    """
    Validator that checks if a value is a valid MIME type.
    """

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message or "Value is not a valid MIME type."

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not MIME_TYPE_PATTERN.match(value):
            raise ValidationError(self.error_message)

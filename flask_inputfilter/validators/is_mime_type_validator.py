from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator

MIME_TYPE_PATTERN = re.compile(RegexEnum.MIME_TYPE.value)


class IsMimeTypeValidator(BaseValidator):
    """
    Checks if a value is a valid MIME type such as ``image/png`` or
    ``application/json``.

    **Parameters:**

    - **allowed_types** (*Optional[list[str]]*): Restricts the check to a
      list of allowed MIME types. If not set, any syntactically valid
      MIME type is accepted.
    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a valid MIME type.

    **Expected Behavior:**

    Ensures the input is a string and matches a regular expression pattern
    for MIME types. If ``allowed_types`` is set, the value must also be
    contained in that list. Raises a ``ValidationError`` otherwise.

    **Example Usage:**

    .. code-block:: python

        class UploadInputFilter(InputFilter):
            content_type: str = field(validators=[
                IsMimeTypeValidator(allowed_types=["image/png", "image/jpeg"])
            ])
    """

    __slots__ = ("allowed_types", "error_message")

    def __init__(
        self,
        allowed_types: Optional[list[str]] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.allowed_types = allowed_types
        self.error_message = error_message or "Value is not a valid MIME type."

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        if not MIME_TYPE_PATTERN.match(value):
            raise ValidationError(self.error_message)

        if self.allowed_types is not None and value not in self.allowed_types:
            raise ValidationError(self.error_message)

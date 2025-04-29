from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator

RGB_COLOR_PATTERN = re.compile(RegexEnum.RGB_COLOR.value)


class IsRgbColorValidator(BaseValidator):
    """
    Checks if a value is a valid RGB color string. The expected format is
    ``rgb(r, g, b)`` where *r*, *g*, and *b* are integers between 0 and 255.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
        value is not a valid RGB color.

    **Expected Behavior:**

    Verifies that the input is a string, matches the RGB color format using a
    regular expression, and that the extracted numeric values are within the
    range 0 to 255. Raises a ``ValidationError`` if the check fails.

    **Example Usage:**

    .. code-block:: python

        class ColorInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('color', validators=[
                    IsRgbColorValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message or "Value is not a valid RGB color."

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        match = RGB_COLOR_PATTERN.match(value)

        if not match:
            raise ValidationError(self.error_message)

        r, g, b = map(int, match.groups())
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValidationError(self.error_message)

from __future__ import annotations

import base64
import binascii
import io
from typing import Any, Optional

from PIL import Image

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsBase64ImageValidator(BaseValidator):
    """
    Validates that a Base64 encoded string represents a valid image by decoding
    it and verifying its integrity.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if
        validation fails.

    **Expected Behavior:**

    Attempts to decode the Base64 string and open the image using the
    PIL library. If the image is invalid or corrupted, a
    ``ValidationError`` is raised.

    **Example Usage:**

    .. code-block:: python

        class AvatarInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('avatar', validators=[
                    IsBase64ImageValidator()
                ])
    """

    __slots__ = ("error_message",)

    def __init__(
        self,
        error_message: Optional[str] = None,
    ) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        try:
            Image.open(io.BytesIO(base64.b64decode(value))).verify()

        except (binascii.Error, OSError):
            raise ValidationError(
                self.error_message
                or "The image is invalid or does not have an allowed size."
            )

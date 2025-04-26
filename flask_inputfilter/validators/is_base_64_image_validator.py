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
    Validator that checks if a Base64 string is a valid image.
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

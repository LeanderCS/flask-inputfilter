from __future__ import annotations

import base64
import binascii
import io
from typing import Any, Optional

from PIL import Image

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsImageValidator(BaseValidator):
    """
    Validates that the provided value is a valid image. Supports various input
    formats including file paths, base64 encoded strings, bytes, or PIL Image
    objects.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if
      validation fails.

    **Expected Behavior:**

    Attempts to validate the input as an image by:
    - If input is a PIL Image object, it's considered valid
    - If input is a string, tries to open it as a file path or decode as base64
    - If input is bytes, tries to open as image data
    - Raises a ``ValidationError`` if the input cannot be processed as an image

    **Example Usage:**

    .. code-block:: python

        class ImageInputFilter(InputFilter):
            image = field(validators=[
                IsImageValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(
        self,
        error_message: Optional[str] = None,
    ) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if isinstance(value, Image.Image):
            return

        if isinstance(value, str):
            try:
                with Image.open(value) as img:
                    img.verify()
                return
            except OSError:
                pass

            try:
                Image.open(io.BytesIO(base64.b64decode(value))).verify()
                return
            except (binascii.Error, OSError):
                pass

        if isinstance(value, bytes):
            try:
                Image.open(io.BytesIO(value)).verify()
                return
            except OSError:
                pass

        raise ValidationError(
            self.error_message or "Value is not a valid image."
        )

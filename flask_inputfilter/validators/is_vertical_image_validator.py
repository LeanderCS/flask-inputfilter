from __future__ import annotations

import base64
import binascii
import io
from typing import Any, Optional

from PIL import Image
from PIL.Image import Image as ImageType

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsVerticalImageValidator(BaseValidator):
    """
    Validates that the provided image is vertically oriented. Accepts either a
    Base64 encoded string or an image object.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the image
      is not vertically oriented.

    **Expected Behavior:**

    Decodes the image (if provided as a string) and checks that its height
    is greater than or equal to its width. Raises a ``ValidationError`` if
    the image is horizontally oriented.

    **Example Usage:**

    .. code-block:: python

        class VerticalImageInputFilter(InputFilter):
            image = field(validators=[
                IsVerticalImageValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "The image is not vertically oriented."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, (str, ImageType)):
            raise ValidationError(
                "The value is not an image or its base 64 representation."
            )

        try:
            if isinstance(value, str):
                value = Image.open(io.BytesIO(base64.b64decode(value)))

            if value.width > value.height:
                raise ValidationError

        except (ValidationError, binascii.Error, OSError):
            raise ValidationError(self.error_message)

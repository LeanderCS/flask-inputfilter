from __future__ import annotations

import base64
import io
from typing import Any, Optional

from PIL import Image

from flask_inputfilter.enums import ImageFormatEnum
from flask_inputfilter.models import BaseFilter


class ToBase64ImageFilter(BaseFilter):
    """
    Converts an image to a base64 encoded string. Supports various input
    formats including file paths, bytes, or PIL Image objects.

    **Parameters:**

    - **format** (*ImageFormatEnum*, default: ``ImageFormatEnum.PNG``):
      The output image format for the base64 encoding.
    - **quality** (*int*, default: ``85``): The image quality (1-100) for
      lossy formats like JPEG. Higher values mean better quality.

    **Expected Behavior:**

    Converts the input image to a base64 encoded string:
    - If input is a PIL Image object, converts it directly
    - If input is a string, tries to open it as a file path
    - If input is bytes, tries to open as image data
    - If input is already a base64 string, validates and returns it
    - Returns the original value if conversion fails

    **Example Usage:**

    .. code-block:: python

        class ImageFilter(InputFilter):
            image = field(filters=[
                ToBase64ImageFilter(format=ImageFormatEnum.JPEG)
            ])
    """

    __slots__ = ("format", "quality")

    def __init__(
        self,
        format: Optional[ImageFormatEnum] = None,
        quality: int = 85,
    ) -> None:
        self.format = format if format else ImageFormatEnum.PNG
        self.quality = quality

    def apply(self, value: Any) -> Any:
        if isinstance(value, Image.Image):
            return self._image_to_base64(value)

        # Try to open as file path
        if isinstance(value, str):
            try:
                with Image.open(value) as img:
                    return self._image_to_base64(img)
            except OSError:
                pass

            # Try to decode as base64
            try:
                Image.open(io.BytesIO(base64.b64decode(value))).verify()
                return value
            except (ValueError, OSError, base64.binascii.Error):
                pass

        # Try to open as raw bytes
        if isinstance(value, bytes):
            try:
                img = Image.open(io.BytesIO(value))
                return self._image_to_base64(img)
            except OSError:
                pass

        return value

    def _image_to_base64(self, image: Image.Image) -> str:
        """Convert a PIL Image to base64 encoded string."""
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        buffered = io.BytesIO()

        save_options = {"format": self.format.value}

        if self.format in (ImageFormatEnum.JPEG, ImageFormatEnum.WEBP):
            save_options["quality"] = self.quality
            save_options["optimize"] = True

        image.save(buffered, **save_options)

        return base64.b64encode(buffered.getvalue()).decode("ascii")

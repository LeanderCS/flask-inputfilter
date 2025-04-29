from __future__ import annotations

import base64
import io
from typing import Any

from PIL import Image

from flask_inputfilter.enums import ImageFormatEnum
from flask_inputfilter.filters import BaseFilter


class Base64ImageResizeFilter(BaseFilter):
    """
    Reduces the file size of a base64-encoded image by resizing and compressing
    it.

    **Parameters:**

    - **max_size** (*int*, default: ``4 * 1024 * 1024``): The maximum
        allowed file size in bytes.
    - **format** (*ImageFormatEnum*, default: ``ImageFormatEnum.JPEG``):
        The output image format.
    - **preserve_icc_profile** (*bool*, default: ``False``): If set to
        ``True``, the ICC profile is preserved.
    - **preserve_metadata** (*bool*, default: ``False``): If set to ``True``,
        image metadata is preserved.

    **Expected Behavior:**

    The filter resizes and compresses the image iteratively until its
    size is below the specified maximum. The final output is a base64-encoded
    string of the resized image. If the input is invalid, the original
    value is returned.

    **Example Usage:**

    .. code-block:: python

        class AvatarFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('avatar', filters=[
                    Base64ImageResizeFilter(max_size=4*1024*1024)
                ])
    """

    __slots__ = (
        "max_size",
        "format",
        "preserve_icc_profile",
        "preserve_metadata",
    )

    def __init__(
        self,
        max_size: int = 4 * 1024 * 1024,
        format: ImageFormatEnum = ImageFormatEnum.JPEG,
        preserve_icc_profile: bool = False,
        preserve_metadata: bool = False,
    ) -> None:
        self.max_size = max_size
        self.format = format
        self.preserve_metadata = preserve_metadata
        self.preserve_icc_profile = preserve_icc_profile

    def apply(self, value: Any) -> Any:
        if not isinstance(value, (str, Image.Image)):
            return value

        try:
            if isinstance(value, Image.Image):
                return self.reduce_image(value)

            value = Image.open(io.BytesIO(base64.b64decode(value)))
            return self.reduce_image(value)
        except (OSError, ValueError, TypeError):
            return value

    def reduce_image(self, image: Image) -> Image:
        """Reduce the size of an image by resizing and compressing it."""

        is_animated = getattr(image, "is_animated", False)

        if not is_animated and image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        buffer = self.save_image_to_buffer(image, quality=80)
        if buffer.getbuffer().nbytes <= self.max_size:
            return self.image_to_base64(image)

        new_width, new_height = image.size

        while (
            buffer.getbuffer().nbytes > self.max_size
            and new_width > 10
            and new_height > 10
        ):
            new_width = int(new_width * 0.9)
            new_height = int(new_height * 0.9)
            image = image.resize((new_width, new_height), Image.LANCZOS)

            buffer = self.save_image_to_buffer(image, quality=80)

        quality = 80
        while buffer.getbuffer().nbytes > self.max_size and quality > 0:
            buffer = self.save_image_to_buffer(image, quality)
            quality -= 5

        return self.image_to_base64(image)

    def save_image_to_buffer(
        self, image: Image.Image, quality: int
    ) -> io.BytesIO:
        """Save the image to an in-memory buffer with the specified quality."""

        buffer = io.BytesIO()
        image.save(buffer, format=self.format.value, quality=quality)
        buffer.seek(0)

        return buffer

    def image_to_base64(self, image: Image) -> str:
        """Convert an image to a base64-encoded string."""

        buffered = io.BytesIO()
        options = {
            "format": self.format.value,
            "optimize": True,
        }

        if self.preserve_icc_profile:
            options["icc_profile"] = image.info.get("icc_profile", None)

        if self.preserve_metadata:
            options["exif"] = image.info.get("exif", None)

        image.save(buffered, **options)
        return base64.b64encode(buffered.getvalue()).decode("ascii")

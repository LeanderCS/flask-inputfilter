from __future__ import annotations

import base64
import io
from typing import Any, Optional

from PIL import Image

from flask_inputfilter.filters import BaseFilter


class Base64ImageDownscaleFilter(BaseFilter):
    """
    Filter that downscales a base64 image to a given size
    """

    __slots__ = ("size", "width", "height", "proportionally")

    def __init__(
        self,
        size: int = 1024 * 1024,
        width: Optional[int] = None,
        height: Optional[int] = None,
        proportionally: bool = True,
    ) -> None:
        self.width = int(width or size**0.5)
        self.height = int(height or size**0.5)
        self.proportionally = proportionally

    def apply(self, value: Any) -> Any:
        if not isinstance(value, (str, Image.Image)):
            return value

        try:
            if isinstance(value, Image.Image):
                return self.resize_picture(value)

            image = Image.open(io.BytesIO(base64.b64decode(value)))
            return self.resize_picture(image)

        except (OSError, ValueError, TypeError):
            return value

    def resize_picture(self, image: Image) -> str:
        """
        Resizes the image if it exceeds the specified width/height
        and returns the base64 representation.
        """
        is_animated = getattr(image, "is_animated", False)

        if not is_animated and image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        if (
            image.size[0] * image.size[1] < self.width * self.height
            or is_animated
        ):
            return self.image_to_base64(image)

        if self.proportionally:
            image = self.scale_image(image)
        else:
            image = image.resize((self.width, self.height), Image.LANCZOS)

        return self.image_to_base64(image)

    def scale_image(self, image: Image) -> Image:
        """
        Scale the image proportionally to fit within the target width/height.
        """
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = self.width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = self.height
            new_width = int(new_height * aspect_ratio)

        return image.resize((new_width, new_height), Image.LANCZOS)

    @staticmethod
    def image_to_base64(image: Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")

        return base64.b64encode(buffered.getvalue()).decode("ascii")

from __future__ import annotations

import base64
import io
from typing import Any

from PIL import Image

from flask_inputfilter.models import BaseFilter


class ToImageFilter(BaseFilter):
    """
    Converts various input formats to a PIL Image object. Supports file paths,
    base64 encoded strings, and bytes.

    **Expected Behavior:**

    Converts the input to a PIL Image object:
    - If input is already a PIL Image object, returns it as-is
    - If input is a string, tries to open it as a file path or decode as base64
    - If input is bytes, tries to open as image data
    - Returns the original value if conversion fails

    **Example Usage:**

    .. code-block:: python

        class ImageFilter(InputFilter):
            image = field(filters=[
                ToImageFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Any:
        if isinstance(value, Image.Image):
            return value

        if isinstance(value, str):
            # Try to open as file path
            try:
                return Image.open(value)
            except OSError:
                pass

            # Try to decode as base64
            try:
                return Image.open(io.BytesIO(base64.b64decode(value)))
            except (ValueError, OSError, base64.binascii.Error):
                pass

        # Try to open as raw bytes
        if isinstance(value, bytes):
            try:
                return Image.open(io.BytesIO(value))
            except OSError:
                pass

        return value

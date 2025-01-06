import base64
from typing import Any

from ..Exception import ValidationError
from ..Validator import BaseValidator


class IsBase64ImageCorrectSizeValidator(BaseValidator):
    """
    Validator that checks if a Base64 string has a valid image size.
    By default, the image size must be between 1 and 4MB.
    """

    def __init__(self, minSize: int = 1,
                 maxSize: int = 4 * 1024 * 1024) -> None:

        self.minSize = minSize
        self.maxSize = maxSize

    def validate(self, value: Any) -> None:

        try:
            decoded_image = base64.b64decode(value, validate=True)
            image_size = len(decoded_image)

            if not (self.minSize <= image_size <= self.maxSize):
                raise ValidationError(f"Image size {image_size} is not "
                                      f"within the range {self.minSize}-"
                                      f"{self.maxSize}.")

        except Exception:
            raise ValidationError("Das Bild ist ungültig oder beschädigt.")

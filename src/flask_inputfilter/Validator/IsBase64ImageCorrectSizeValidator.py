import base64
from typing import Any

from src.flask_inputfilter.Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsBase64ImageCorrectSizeValidator(BaseValidator):
    """
    Validator that checks if a Base64 string has a valid image size.
    """

    def __init__(self, minSize: int, maxSize: int) -> None:

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

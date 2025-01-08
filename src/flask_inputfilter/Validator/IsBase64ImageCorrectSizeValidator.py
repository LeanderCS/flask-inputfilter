import base64
from typing import Any

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class IsBase64ImageCorrectSizeValidator(BaseValidator):
    """
    Validator that checks if a Base64 string has a valid image size.
    By default, the image size must be between 1 and 4MB.
    """

    def __init__(
        self,
        minSize: int = 1,
        maxSize: int = 4 * 1024 * 1024,
        error_message: str = "The image is invalid or does not have an allowed size.",
    ) -> None:

        self.min_size = minSize
        self.max_size = maxSize
        self.error_message = error_message

    def validate(self, value: Any) -> None:

        try:
            decoded_image = base64.b64decode(value, validate=True)
            image_size = len(decoded_image)

            if not (self.min_size <= image_size <= self.max_size):
                raise ValidationError

        except Exception:
            raise ValidationError(self.error_message)

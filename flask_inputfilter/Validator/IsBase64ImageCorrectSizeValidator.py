import base64
from typing import Any, Optional

from ..Exception import ValidationError
from .BaseValidator import BaseValidator


class IsBase64ImageCorrectSizeValidator(BaseValidator):
    """
    Validator that checks if a Base64 string has a valid image size.
    By default, the image size must be between 1 and 4MB.
    """

    def __init__(
        self,
        minSize: int = 1,
        maxSize: int = 4 * 1024 * 1024,
        error_message: Optional[str] = None,
    ) -> None:
        self.min_size = minSize
        self.max_size = maxSize
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        try:
            image_size = len(base64.b64decode(value, validate=True))

            if not (self.min_size <= image_size <= self.max_size):
                raise ValidationError

        except Exception:
            raise ValidationError(
                self.error_message
                or "The image is invalid or does not have an allowed size."
            )

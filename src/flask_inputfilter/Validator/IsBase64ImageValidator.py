import base64
import io
from PIL import Image
from typing import Any

from ..Exception import ValidationError
from ..Validator import BaseValidator


class IsBase64ImageValidator(BaseValidator):
    """
    Validator that checks if a Base64 string is a valid image.
    """

    def __init__(
        self,
        error_message: str = "The image is invalid or does not have an allowed size.",
    ) -> None:

        self.error_message = error_message

    def validate(self, value: Any) -> None:

        try:
            decodedData = base64.b64decode(value)
            image = Image.open(io.BytesIO(decodedData))
            image.verify()

        except Exception:
            raise ValidationError(self.error_message)

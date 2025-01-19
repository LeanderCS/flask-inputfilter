import base64
import io
from typing import Any, Optional

from PIL import Image

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsBase64ImageValidator(BaseValidator):
    """
    Validator that checks if a Base64 string is a valid image.
    """

    def __init__(
        self,
        error_message: Optional[str] = None,
    ) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        try:
            decodedData = base64.b64decode(value)
            image = Image.open(io.BytesIO(decodedData))
            image.verify()

        except Exception:
            raise ValidationError(
                self.error_message
                or "The image is invalid or does not have an allowed size."
            )

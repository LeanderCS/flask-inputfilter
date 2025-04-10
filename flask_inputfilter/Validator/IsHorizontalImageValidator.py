import base64
import io

from PIL import Image
from PIL.Image import Image as ImageType

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsHorizontalImageValidator(BaseValidator):
    """
    Validates if an image is horizontally oriented.

    This class checks if the given image is in a horizontal orientation by
    comparing its width and height. If the image is not horizontally oriented,
    a validation error is raised. The error message can be customized during
    initialization of the validator.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message=None):
        self.error_message = (
            error_message or "The image is not horizontally oriented."
        )

    def validate(self, value):
        if not isinstance(value, (str, ImageType)):
            raise ValidationError(
                "The value is not an image or its base 64 representation."
            )

        try:
            if isinstance(value, str):
                value = Image.open(io.BytesIO(base64.b64decode(value)))

            if value.width < value.height:
                raise

        except Exception:
            raise ValidationError(self.error_message)

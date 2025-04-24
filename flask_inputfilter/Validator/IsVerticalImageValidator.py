from __future__ import annotations

import base64
import binascii
import io
from typing import Any

from PIL import Image
from PIL.Image import Image as ImageType

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsVerticalImageValidator(BaseValidator):
    """
    Responsible for validating whether an image is vertically oriented.

    This class is designed to validate if a given image or its base64
    representation has a height greater than its width. It supports
    validation for multiple image formats and raises an appropriate
    error if the validation fails.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message=None):
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, (str, ImageType)):
            raise ValidationError(
                "The value is not an image or its base 64 representation."
            )

        try:
            if isinstance(value, str):
                value = Image.open(io.BytesIO(base64.b64decode(value)))

            if value.width > value.height:
                raise ValidationError

        except (binascii.Error, OSError):
            raise ValidationError(
                self.error_message or "The image is not vertically oriented."
            )

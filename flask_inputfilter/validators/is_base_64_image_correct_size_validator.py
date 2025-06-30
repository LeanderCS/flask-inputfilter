from __future__ import annotations

import base64
import binascii
import warnings
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class IsBase64ImageCorrectSizeValidator(BaseValidator):
    """
    Hecks whether a Base64 encoded image has a size within the allowed range.
    By default, the image size must be between 1 and 4MB.

    **Parameters:**

    - **minSize** (*int*, default: 1): The minimum allowed size
        in bytes.
    - **maxSize** (*int*, default: 4 * 1024 * 1024): The maximum
        allowed size in bytes.
    - **error_message** (*Optional[str]*): Custom error message
        if validation fails.

    **Expected Behavior:**

    Decodes the Base64 string to determine the image size and raises
    a ``ValidationError`` if the image size is outside the permitted range.

    **Example Usage:**

    .. code-block:: python

        class ImageInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('image', validators=[
                    IsBase64ImageCorrectSizeValidator(
                        min_size=1024,
                        max_size=2 * 1024 * 1024
                    )
                ])
    """

    __slots__ = ("min_size", "max_size", "error_message")

    def __init__(
        self,
        min_size: Optional[int] = None,
        max_size: Optional[int] = None,
        error_message: Optional[str] = None,
        # Deprecated parameters (for Backward Compatibility)
        minSize: Optional[int] = None,
        maxSize: Optional[int] = None,
    ) -> None:
        if minSize is not None:
            warnings.warn(
                "Parameter 'minSize' is deprecated, use 'min_size' instead",
                DeprecationWarning,
                stacklevel=2,
            )
            if min_size is None:
                min_size = minSize

        if maxSize is not None:
            warnings.warn(
                "Parameter 'maxSize' is deprecated, use 'max_size' instead",
                DeprecationWarning,
                stacklevel=2,
            )
            if max_size is None:
                max_size = maxSize

        self.min_size = min_size if min_size is not None else 1
        self.max_size = max_size if max_size is not None else 4 * 1024 * 1024
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        try:
            image_size = len(base64.b64decode(value, validate=True))

            if not (self.min_size <= image_size <= self.max_size):
                raise ValidationError

        except (binascii.Error, ValidationError):
            raise ValidationError(
                self.error_message
                or "The image is invalid or does not have an allowed size."
            )

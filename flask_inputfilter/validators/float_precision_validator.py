from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class FloatPrecisionValidator(BaseValidator):
    """
    Ensures that a numeric value conforms to a specific precision and scale.
    This is useful for validating monetary values or measurements.

    **Parameters:**

    - **precision** (*int*): The maximum total number of digits allowed.
    - **scale** (*int*): The maximum number of digits allowed after the
        decimal point.
    - **error_message** (*Optional[str]*): Custom error message if
        validation fails.

    **Expected Behavior:**

    Converts the number to a string and checks the total number of digits and
    the digits after the decimal point. A ``ValidationError`` is raised if
    these limits are exceeded.

    **Example Usage:**

    .. code-block:: python

        class PriceInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('price', validators=[
                    FloatPrecisionValidator(precision=5, scale=2)
                ])
    """

    __slots__ = ("precision", "scale", "error_message")

    def __init__(
        self,
        precision: int,
        scale: int,
        error_message: Optional[str] = None,
    ) -> None:
        self.precision = precision
        self.scale = scale
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, (float, int)):
            raise ValidationError(
                f"Value '{value}' must be a float or an integer."
            )

        value_str = str(value)
        match = re.match(r"^-?(\d+)(\.(\d+))?$", value_str)
        if not match:
            raise ValidationError(f"Value '{value}' is not a valid float.")

        digits_before = len(match.group(1))
        digits_after = len(match.group(3)) if match.group(3) else 0
        total_digits = digits_before + digits_after

        if total_digits > self.precision or digits_after > self.scale:
            raise ValidationError(
                self.error_message
                or f"Value '{value}' has more than {self.precision} digits "
                f"in total or '{self.scale}' digits after the "
                f"decimal point."
            )

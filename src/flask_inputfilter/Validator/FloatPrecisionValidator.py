import re
from typing import Any

from ..Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


class FloatPrecisionValidator(BaseValidator):
    """
    Validator that checks the precision and scale of a float.
    """

    def __init__(
        self,
        precision: int,
        scale: int,
        error_message: str = "Value '{}' has more than {} digits in total or "
        "{} digits after the decimal point.",
    ) -> None:

        self.precision = precision
        self.scale = scale
        self.error_message = error_message

    def validate(self, value: Any) -> None:

        if not isinstance(value, (float, int)):
            raise ValidationError("Value must be a float or an integer")

        value_str = str(value)
        match = re.match(r"^-?(\d+)(\.(\d+))?$", value_str)
        if not match:
            raise ValidationError("Value is not a valid float")

        digits_before = len(match.group(1))
        digits_after = len(match.group(3)) if match.group(3) else 0
        total_digits = digits_before + digits_after

        if total_digits > self.precision or digits_after > self.scale:
            if "{}" in self.error_message:
                raise ValidationError(
                    self.error_message.format(
                        value, self.precision, self.scale
                    )
                )

            raise ValidationError(self.error_message)

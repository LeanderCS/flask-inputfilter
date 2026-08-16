from __future__ import annotations

import re
from typing import Any, Optional

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator

CREDIT_CARD_PATTERN = re.compile(RegexEnum.CREDIT_CARD.value)


class IsCreditCardValidator(BaseValidator):
    """
    Checks if a value is a valid credit card number. Supports the major card
    schemes (Visa, Mastercard, American Express, Diners Club, Discover and JCB)
    and verifies the checksum using the Luhn algorithm.

    **Parameters:**

    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a valid credit card number.

    **Expected Behavior:**

    Ensures the input is a string, strips spaces and hyphens, matches the
    result against known card number formats and validates the Luhn
    checksum. Raises a ``ValidationError`` if any of these checks fail.

    **Example Usage:**

    .. code-block:: python

        class PaymentInputFilter(InputFilter):
            card_number: str = field(validators=[
                IsCreditCardValidator()
            ])
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value is not a valid credit card number."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        number = value.replace(" ", "").replace("-", "")

        if not CREDIT_CARD_PATTERN.match(number) or not self._luhn_valid(
            number
        ):
            raise ValidationError(self.error_message)

    @staticmethod
    def _luhn_valid(number: str) -> bool:
        checksum = 0
        for index, digit in enumerate(reversed(number)):
            digit = int(digit)
            if index % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        return checksum % 10 == 0

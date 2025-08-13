from __future__ import annotations

import re
from typing import Any, ClassVar, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class CreditCardValidator(BaseValidator):
    """
    Validates credit card numbers using Luhn algorithm and card type patterns.

    This validator checks credit card numbers for validity using the Luhn
    algorithm and can optionally validate specific card types.
    """

    CARD_TYPES: ClassVar = {
        "visa": {
            "pattern": r"^4[0-9]{12}(?:[0-9]{3})?$",
            "lengths": [13, 16, 19],
            "display": "Visa",
        },
        "mastercard": {
            "pattern": r"^5[1-5][0-9]{14}$|^2[2-7][0-9]{14}$",
            "lengths": [16],
            "display": "MasterCard",
        },
        "amex": {
            "pattern": r"^3[47][0-9]{13}$",
            "lengths": [15],
            "display": "American Express",
        },
        "discover": {
            "pattern": r"^6(?:011|5[0-9]{2})[0-9]{12}$",
            "lengths": [16],
            "display": "Discover",
        },
        "diners": {
            "pattern": r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$",
            "lengths": [14],
            "display": "Diners Club",
        },
        "jcb": {
            "pattern": r"^(?:2131|1800|35\d{3})\d{11}$",
            "lengths": [15, 16],
            "display": "JCB",
        },
        "unionpay": {
            "pattern": r"^62[0-9]{14,17}$",
            "lengths": [16, 17, 18, 19],
            "display": "UnionPay",
        },
        "maestro": {
            "pattern": r"^(?:5[06-9]|6)[0-9]{10,17}$",
            "lengths": list(range(12, 20)),
            "display": "Maestro",
        },
    }

    def __init__(
        self,
        accepted_types: Optional[List[str]] = None,
        require_type: bool = False,
        allow_test_numbers: bool = False,
        validate_expiry: bool = False,
        validate_cvv: bool = False,
    ) -> None:
        """
        Initialize the credit card validator.

        Args:
            accepted_types: List of accepted card types (visa, mastercard,
                etc.)
            require_type: Whether to require the card to match a known type
            allow_test_numbers: Whether to allow known test card numbers
            validate_expiry: Whether to validate expiry date (if provided)
            validate_cvv: Whether to validate CVV (if provided)
        """
        self.accepted_types = accepted_types
        self.require_type = require_type
        self.allow_test_numbers = allow_test_numbers
        self.validate_expiry = validate_expiry
        self.validate_cvv = validate_cvv

        self.test_numbers = {
            "4111111111111111",  # Visa test
            "5555555555554444",  # Mastercard test
            "378282246310005",  # Amex test
            "6011111111111117",  # Discover test
            "3530111333300000",  # JCB test
        }

    def validate(self, value: Any) -> None:
        """
        Validate the credit card number.

        Args:
            value: The credit card number to validate

        Raises:
            ValidationError: If the credit card number is invalid
        """
        if value is None:
            raise ValidationError("Credit card number cannot be None")

        if not isinstance(value, str):
            value = str(value)

        cleaned = re.sub(r"[\s\-]", "", value)

        if not cleaned.isdigit():
            raise ValidationError(
                "Credit card number must contain only digits"
            )

        if len(cleaned) < 13 or len(cleaned) > 19:
            raise ValidationError(
                f"Credit card number must be between 13 and 19 digits, "
                f"got {len(cleaned)}"
            )

        if not self.allow_test_numbers and cleaned in self.test_numbers:
            raise ValidationError("Test credit card numbers are not allowed")

        if not self._luhn_check(cleaned):
            raise ValidationError(
                "Invalid credit card number (failed Luhn check)"
            )

        card_type = self._detect_card_type(cleaned)

        if self.require_type and card_type is None:
            raise ValidationError("Credit card type could not be determined")

        if (
            self.accepted_types
            and card_type
            and card_type not in self.accepted_types
        ):
            display_name = self.CARD_TYPES[card_type]["display"]
            accepted = ", ".join(
                self.CARD_TYPES[t]["display"] for t in self.accepted_types
            )
            raise ValidationError(
                f"{display_name} cards are not accepted. Accepted types: {accepted}"
            )

    def _luhn_check(self, number: str) -> bool:
        """
        Validate credit card number using Luhn algorithm.

        Args:
            number: The credit card number as a string of digits

        Returns:
            True if valid, False otherwise
        """

        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]

        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))

        return checksum % 10 == 0

    def _detect_card_type(self, number: str) -> Optional[str]:
        """
        Detect the credit card type from the number.

        Args:
            number: The credit card number

        Returns:
            Card type string or None if not detected
        """
        for card_type, info in self.CARD_TYPES.items():
            if (
                re.match(info["pattern"], number)
                and len(number) in info["lengths"]
            ):
                return card_type

        return None

    def get_card_info(self, number: str) -> Optional[dict]:
        """
        Get information about a credit card number.

        Args:
            number: The credit card number

        Returns:
            Dictionary with card information or None
        """
        cleaned = re.sub(r"[\s\-]", "", str(number))
        card_type = self._detect_card_type(cleaned)

        if card_type:
            return {
                "type": card_type,
                "display_name": self.CARD_TYPES[card_type]["display"],
                "valid": self._luhn_check(cleaned),
                "length": len(cleaned),
                "masked": self._mask_number(cleaned),
            }

        return None

    def _mask_number(self, number: str) -> str:
        """
        Mask credit card number for display.

        Args:
            number: The credit card number

        Returns:
            Masked number (e.g., "****-****-****-1234")
        """
        if len(number) <= 4:
            return number

        masked = "*" * (len(number) - 4) + number[-4:]

        groups = []
        for i in range(0, len(masked), 4):
            groups.append(masked[i : i + 4])

        return "-".join(groups)

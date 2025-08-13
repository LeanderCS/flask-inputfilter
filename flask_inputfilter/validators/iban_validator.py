from __future__ import annotations

import re
from typing import Any, ClassVar, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IbanValidator(BaseValidator):
    """
    Validates International Bank Account Numbers (IBAN).

    This validator checks IBAN format and validates the check digits according
    to the IBAN standard (ISO 13616).
    """

    IBAN_LENGTHS: ClassVar = {
        "AD": 24,
        "AE": 23,
        "AL": 28,
        "AT": 20,
        "AZ": 28,
        "BA": 20,
        "BE": 16,
        "BG": 22,
        "BH": 22,
        "BR": 29,
        "BY": 28,
        "CH": 21,
        "CR": 22,
        "CY": 28,
        "CZ": 24,
        "DE": 22,
        "DK": 18,
        "DO": 28,
        "EE": 20,
        "EG": 29,
        "ES": 24,
        "FI": 18,
        "FO": 18,
        "FR": 27,
        "GB": 22,
        "GE": 22,
        "GI": 23,
        "GL": 18,
        "GR": 27,
        "GT": 28,
        "HR": 21,
        "HU": 28,
        "IE": 22,
        "IL": 23,
        "IS": 26,
        "IT": 27,
        "JO": 30,
        "KW": 30,
        "KZ": 20,
        "LB": 28,
        "LC": 32,
        "LI": 21,
        "LT": 20,
        "LU": 20,
        "LV": 21,
        "MC": 27,
        "MD": 24,
        "ME": 22,
        "MK": 19,
        "MR": 27,
        "MT": 31,
        "MU": 30,
        "NL": 18,
        "NO": 15,
        "PK": 24,
        "PL": 28,
        "PS": 29,
        "PT": 25,
        "QA": 29,
        "RO": 24,
        "RS": 22,
        "SA": 24,
        "SE": 24,
        "SI": 19,
        "SK": 24,
        "SM": 27,
        "TN": 24,
        "TR": 26,
        "UA": 29,
        "VA": 22,
        "VG": 24,
        "XK": 20,
    }

    def __init__(
        self,
        allowed_countries: Optional[List[str]] = None,
        format_output: bool = False,
        check_bank_code: bool = False,
        allow_spaces: bool = True,
    ) -> None:
        """
        Initialize the IBAN validator.

        Args:
            allowed_countries: List of allowed country codes
              (e.g., ['DE', 'FR'])
            format_output: Whether to format the IBAN in groups of 4
            check_bank_code: Whether to validate bank code
              (requires additional data)
            allow_spaces: Whether to allow spaces in input
        """
        self.allowed_countries = (
            [c.upper() for c in allowed_countries]
            if allowed_countries
            else None
        )
        self.format_output = format_output
        self.check_bank_code = check_bank_code
        self.allow_spaces = allow_spaces

    def validate(self, value: Any) -> None:
        """
        Validate the IBAN.

        Args:
            value: The IBAN to validate

        Raises:
            ValidationError: If the IBAN is invalid
        """
        if value is None:
            raise ValidationError("IBAN cannot be None")

        if not isinstance(value, str):
            raise ValidationError(
                f"IBAN must be a string, not {type(value).__name__}"
            )

        iban = self._clean_iban(value)

        if not re.match(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]+$", iban):
            raise ValidationError(
                "Invalid IBAN format. Must start with 2 letters "
                "(country code) followed by 2 digits (check digits) "
                "and alphanumeric characters"
            )

        country_code = iban[:2]

        if (
            self.allowed_countries
            and country_code not in self.allowed_countries
        ):
            allowed = ", ".join(self.allowed_countries)
            raise ValidationError(
                f"Country code {country_code} not allowed. "
                f"Allowed countries: {allowed}"
            )

        if country_code in self.IBAN_LENGTHS:
            expected_length = self.IBAN_LENGTHS[country_code]
            if len(iban) != expected_length:
                raise ValidationError(
                    f"Invalid IBAN length for {country_code}. "
                    f"Expected {expected_length} characters, got {len(iban)}"
                )
        else:
            if len(iban) < 15 or len(iban) > 34:
                raise ValidationError(
                    "Invalid IBAN length. Must be between 15 and 34 characters"
                )

        if not IbanValidator._validate_check_digits(iban):
            raise ValidationError("Invalid IBAN check digits")

        self._validate_country_specific(country_code, iban)

    def _clean_iban(self, iban: str) -> str:
        """
        Clean and normalize IBAN.

        Args:
            iban: The IBAN string

        Returns:
            Cleaned IBAN
        """
        if self.allow_spaces:
            iban = re.sub(r"[\s\-]", "", iban)

        return iban.upper()

    @staticmethod
    def _validate_check_digits(iban: str) -> bool:
        """
        Validate IBAN check digits using mod-97 algorithm.

        Args:
            iban: The IBAN string

        Returns:
            True if valid, False otherwise
        """
        rearranged = iban[4:] + iban[:4]

        numeric_string = ""
        for char in rearranged:
            if char.isdigit():
                numeric_string += char
            else:
                numeric_string += str(ord(char) - ord("A") + 10)

        return int(numeric_string) % 97 == 1

    def _validate_country_specific(self, country_code: str, iban: str) -> None:
        """
        Perform country-specific validation.

        Args:
            country_code: The country code
            iban: The complete IBAN

        Raises:
            ValidationError: If country-specific validation fails
        """
        if country_code == "DE" and self.check_bank_code:
            bank_code = iban[4:12]
            if not bank_code.isdigit():
                raise ValidationError("Invalid German bank code")

        elif country_code == "GB" and self.check_bank_code:
            if not iban[4:].isalnum():
                raise ValidationError("Invalid UK IBAN format")

        elif country_code == "FR" and self.check_bank_code:
            pass

    def format(self, iban: str) -> str:
        """
        Format IBAN in groups of 4 characters.

        Args:
            iban: The IBAN to format

        Returns:
            Formatted IBAN
        """
        iban = self._clean_iban(iban)

        if self.format_output:
            groups = []
            for i in range(0, len(iban), 4):
                groups.append(iban[i : i + 4])
            return " ".join(groups)

        return iban

    def get_country_name(self, iban: str) -> Optional[str]:
        """
        Get the country name from IBAN.

        Args:
            iban: The IBAN

        Returns:
            Country name or None
        """
        country_names = {
            "AD": "Andorra",
            "AE": "United Arab Emirates",
            "AT": "Austria",
            "BE": "Belgium",
            "BG": "Bulgaria",
            "CH": "Switzerland",
            "CY": "Cyprus",
            "CZ": "Czech Republic",
            "DE": "Germany",
            "DK": "Denmark",
            "EE": "Estonia",
            "ES": "Spain",
            "FI": "Finland",
            "FR": "France",
            "GB": "United Kingdom",
            "GR": "Greece",
            "HR": "Croatia",
            "HU": "Hungary",
            "IE": "Ireland",
            "IL": "Israel",
            "IS": "Iceland",
            "IT": "Italy",
            "LI": "Liechtenstein",
            "LT": "Lithuania",
            "LU": "Luxembourg",
            "LV": "Latvia",
            "MC": "Monaco",
            "MT": "Malta",
            "NL": "Netherlands",
            "NO": "Norway",
            "PL": "Poland",
            "PT": "Portugal",
            "RO": "Romania",
            "SE": "Sweden",
            "SI": "Slovenia",
            "SK": "Slovakia",
        }

        iban = self._clean_iban(iban)
        country_code = iban[:2] if len(iban) >= 2 else None

        return country_names.get(country_code)

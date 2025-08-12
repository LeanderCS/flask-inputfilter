from __future__ import annotations

"""Phone number normalization filter for international formats."""

import re
from typing import Any

from flask_inputfilter.models import BaseFilter


class PhoneNumberNormalizeFilter(BaseFilter):
    """
    Normalizes phone numbers to standard formats.

    This filter converts phone numbers to standardized formats like E.164 and
    can handle international and domestic numbers.
    """

    COUNTRY_CODES = {
        "US": {"code": "1", "length": 10, "format": "NPA-NXX-XXXX"},
        "CA": {"code": "1", "length": 10, "format": "NPA-NXX-XXXX"},
        "GB": {"code": "44", "length": 10, "format": "XXXX-XXXXXX"},
        "DE": {"code": "49", "length": 11, "format": "XXX-XXXXXXXX"},
        "FR": {"code": "33", "length": 9, "format": "X-XX-XX-XX-XX"},
        "JP": {"code": "81", "length": 10, "format": "XX-XXXX-XXXX"},
        "AU": {"code": "61", "length": 9, "format": "XXX-XXX-XXX"},
        "IN": {"code": "91", "length": 10, "format": "XXXXX-XXXXX"},
        "CN": {"code": "86", "length": 11, "format": "XXX-XXXX-XXXX"},
        "BR": {"code": "55", "length": 11, "format": "XX-XXXXX-XXXX"},
        "MX": {"code": "52", "length": 10, "format": "XXX-XXX-XXXX"},
        "RU": {"code": "7", "length": 10, "format": "XXX-XXX-XX-XX"},
        "IT": {"code": "39", "length": 10, "format": "XXX-XXX-XXXX"},
        "ES": {"code": "34", "length": 9, "format": "XXX-XX-XX-XX"},
        "NL": {"code": "31", "length": 9, "format": "XX-XXX-XXXX"},
        "CH": {"code": "41", "length": 9, "format": "XX-XXX-XX-XX"},
        "SE": {"code": "46", "length": 9, "format": "XX-XXX-XX-XX"},
        "NO": {"code": "47", "length": 8, "format": "XXXX-XXXX"},
        "PL": {"code": "48", "length": 9, "format": "XXX-XXX-XXX"},
        "BE": {"code": "32", "length": 9, "format": "XXX-XX-XX-XX"},
    }

    def __init__(
        self,
        default_country: str = "US",
        format: str = "E164",
        remove_extension: bool = False,
        allow_alpha: bool = False,
        strict: bool = False,
    ) -> None:
        """
        Initialize the phone number normalizer.

        Args:
            default_country: Default country code for numbers without country prefix
            format: Output format ('E164', 'INTERNATIONAL', 'NATIONAL', 'RFC3966')
            remove_extension: Whether to remove extensions
            allow_alpha: Whether to allow alpha characters (1-800-FLOWERS)
            strict: Whether to enforce strict validation
        """
        self.default_country = default_country.upper()
        self.format = format.upper()
        self.remove_extension = remove_extension
        self.allow_alpha = allow_alpha
        self.strict = strict

    def apply(self, value: Any) -> str:
        """
        Normalize the phone number.

        Args:
            value: The phone number to normalize

        Returns:
            Normalized phone number string
        """
        if value is None:
            return ""

        if not isinstance(value, str):
            value = str(value)

        # Remove common formatting characters
        cleaned = self._clean_number(value)

        # Handle alpha characters if allowed
        if self.allow_alpha:
            cleaned = self._convert_alpha_to_digits(cleaned)

        # Extract extension if present
        number, extension = self._extract_extension(cleaned)

        # Detect country code
        country_code, national_number = self._extract_country_code(number)

        # If no country code detected, use default
        if not country_code and self.default_country in self.COUNTRY_CODES:
            country_code = self.COUNTRY_CODES[self.default_country]["code"]

        # Validate and format based on output format
        if self.format == "E164":
            result = self._format_e164(country_code, national_number)
        elif self.format == "INTERNATIONAL":
            result = self._format_international(country_code, national_number)
        elif self.format == "NATIONAL":
            result = self._format_national(
                national_number, self.default_country
            )
        elif self.format == "RFC3966":
            result = self._format_rfc3966(country_code, national_number)
        else:
            result = (
                f"+{country_code}{national_number}"
                if country_code
                else national_number
            )

        # Add extension if not removed
        if extension and not self.remove_extension:
            result = f"{result} x{extension}"

        return result

    def _clean_number(self, number: str) -> str:
        """Remove common formatting characters from phone number."""
        cleaned = re.sub(r"[\s\-\.\(\)\[\]]", "", number)

        cleaned = re.sub(r"^0+(?=[1-9])", "", cleaned)

        cleaned = re.sub(r"^\+", "", cleaned)
        cleaned = re.sub(r"^00", "", cleaned)

        return cleaned

    def _convert_alpha_to_digits(self, number: str) -> str:
        """Convert alpha characters to digits (for vanity numbers)."""
        alpha_map = {
            "A": "2",
            "B": "2",
            "C": "2",
            "D": "3",
            "E": "3",
            "F": "3",
            "G": "4",
            "H": "4",
            "I": "4",
            "J": "5",
            "K": "5",
            "L": "5",
            "M": "6",
            "N": "6",
            "O": "6",
            "P": "7",
            "Q": "7",
            "R": "7",
            "S": "7",
            "T": "8",
            "U": "8",
            "V": "8",
            "W": "9",
            "X": "9",
            "Y": "9",
            "Z": "9",
        }

        result = []
        for char in number.upper():
            if char in alpha_map:
                result.append(alpha_map[char])
            elif char.isdigit():
                result.append(char)

        return "".join(result)

    def _extract_extension(self, number: str) -> tuple:
        """Extract extension from phone number."""
        extension_patterns = [
            r"(?:x|ext|extension|ext\.)[\s]?(\d+)$",
            r",(\d+)$",
            r";(\d+)$",
            r"#(\d+)$",
        ]

        for pattern in extension_patterns:
            match = re.search(pattern, number, re.IGNORECASE)
            if match:
                extension = match.group(1)
                number = number[: match.start()].strip()
                return number, extension

        return number, None

    def _extract_country_code(self, number: str) -> tuple:
        """Extract country code from phone number."""
        for country, info in self.COUNTRY_CODES.items():
            code = info["code"]
            if number.startswith(code):
                remaining = number[len(code) :]
                if len(remaining) == info["length"]:
                    return code, remaining

        if number.startswith("1") and len(number) == 11:
            return "1", number[1:]

        return None, number

    def _format_e164(self, country_code: str, national: str) -> str:
        """Format as E.164 (+1234567890)."""
        if country_code:
            return f"+{country_code}{national}"
        return national

    def _format_international(self, country_code: str, national: str) -> str:
        """Format as international (+1 234-567-8900)."""
        if country_code:
            if country_code == "1":
                if len(national) == 10:
                    return f"+{country_code} {national[:3]}-{national[3:6]}-{national[6:]}"
            elif country_code == "44":
                if len(national) == 10:
                    return f"+{country_code} {national[:4]} {national[4:]}"

            return f"+{country_code} {national}"

        return national

    def _format_national(self, national: str, country: str) -> str:
        """Format as national number for specific country."""
        if country == "US" or country == "CA":
            if len(national) == 10:
                return f"({national[:3]}) {national[3:6]}-{national[6:]}"
        elif country == "GB":
            if len(national) == 10:
                return f"{national[:4]} {national[4:]}"

        return national

    def _format_rfc3966(self, country_code: str, national: str) -> str:
        """Format as RFC3966 (tel:+1-234-567-8900)."""
        if country_code:
            if country_code == "1" and len(national) == 10:
                return f"tel:+{country_code}-{national[:3]}-{national[3:6]}-{national[6:]}"
            return f"tel:+{country_code}-{national}"

        return f"tel:{national}"

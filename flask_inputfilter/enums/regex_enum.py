from __future__ import annotations

from enum import Enum


class RegexEnum(Enum):
    """Enum for regex patterns."""

    EMAIL = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    IPV4_ADDRESS = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    IPV6_ADDRESS = r"^\[?([a-fA-F0-9:]+:+)+[a-fA-F0-9]+\]?$"

    MAC_ADDRESS = r"^([0-9A-Fa-f]{2}([-:])){5}[0-9A-Fa-f]{2}$"

    ISO_DATE = r"^\d{4}-\d{2}-\d{2}$"
    ISO_DATETIME = (
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
        r"(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$"
    )

    PHONE_NUMBER = r"^\+?[\d\s\-()]{7,}$"

    POSTAL_CODE = r"^\d{4,10}$"

    URL = r"^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$"

    UUID = (
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    )

    CREDIT_CARD = (
        r"^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3"
        r"(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|"
        r"(?:2131|1800|35\d{3})\d{11})$"
    )

    RGB_COLOR = r"^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$"
    HEX_COLOR = r"^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$"

    INTEGER_PATTERN = r"^[0-9]+$"
    FLOAT_PATTERN = r"^[0-9]*\.[0-9]+$"

    MIME_TYPE = r"^[a-z0-9]+\/[a-z0-9\-\+]+$"

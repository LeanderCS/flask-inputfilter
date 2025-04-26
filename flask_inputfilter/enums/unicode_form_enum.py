from __future__ import annotations

from enum import Enum


class UnicodeFormEnum(Enum):
    NFC = "NFC"
    NFD = "NFD"
    NFKC = "NFKC"
    NFKD = "NFKD"

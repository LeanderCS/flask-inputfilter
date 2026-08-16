from __future__ import annotations

import re


def _name_parts(name: str) -> list[str]:
    cleaned = re.sub(r"[^0-9A-Za-z]+", "_", name)
    parts = [part for part in cleaned.split("_") if part]
    if parts and parts[0][0].isdigit():
        parts[0] = f"N{parts[0]}"
    return parts


def to_pascal_case(name: str, *, normalize: bool = False) -> str:
    parts = _name_parts(name)
    if normalize:
        return "".join(part.capitalize() for part in parts)
    return "".join(part[:1].upper() + part[1:] for part in parts)


def to_input_filter_class_name(name: str) -> str:
    return f"{to_pascal_case(name, normalize=True)}InputFilter"

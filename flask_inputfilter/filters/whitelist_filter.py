from __future__ import annotations

from typing import Any, List

from flask_inputfilter.filters import BaseFilter


class WhitelistFilter(BaseFilter):
    """Filter that filters out values that are not in the whitelist."""

    __slots__ = ("whitelist",)

    def __init__(self, whitelist: List[str] = None) -> None:
        self.whitelist = whitelist

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            return " ".join(
                [word for word in value.split() if word in self.whitelist]
            )

        elif isinstance(value, list):
            return [item for item in value if item in self.whitelist]

        elif isinstance(value, dict):
            return {
                key: value
                for key, value in value.items()
                if key in self.whitelist
            }

        return value

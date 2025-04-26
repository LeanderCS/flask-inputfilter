from __future__ import annotations

from typing import Any, List

from flask_inputfilter.filters import BaseFilter


class BlacklistFilter(BaseFilter):
    """
    Filter that filters out values that are in the blacklist.
    """

    __slots__ = ("blacklist",)

    def __init__(self, blacklist: List[str]) -> None:
        self.blacklist = blacklist

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            for item in self.blacklist:
                value = value.replace(item, "")
            return value.strip()

        elif isinstance(value, list):
            return [item for item in value if item not in self.blacklist]

        elif isinstance(value, dict):
            return {
                key: value
                for key, value in value.items()
                if key not in self.blacklist
            }

        return value

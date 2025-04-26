from __future__ import annotations

from typing import Dict

from flask_inputfilter.conditions import BaseCondition


class StringLongerThanCondition(BaseCondition):
    """
    Condition that checks if the length of the string is longer
    than the given length.
    """

    __slots__ = ("longer_field", "shorter_field")

    def __init__(self, longer_field: str, shorter_field: str) -> None:
        self.longer_field = longer_field
        self.shorter_field = shorter_field

    def check(self, value: Dict[str, str]) -> bool:
        return len(value.get(self.longer_field) or 0) > len(
            value.get(self.shorter_field) or 0
        )

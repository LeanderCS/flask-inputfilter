from __future__ import annotations

from typing import Dict

from flask_inputfilter.conditions import BaseCondition


class IntegerBiggerThanCondition(BaseCondition):
    """
    Condition that ensures an integer is bigger than the specified value.
    """

    __slots__ = ("bigger_field", "smaller_field")

    def __init__(self, bigger_field: str, smaller_field: str) -> None:
        self.bigger_field = bigger_field
        self.smaller_field = smaller_field

    def check(self, data: Dict[str, int]) -> bool:
        if (
            data.get(self.bigger_field) is None
            or data.get(self.smaller_field) is None
        ):
            return False

        return data.get(self.bigger_field) > data.get(self.smaller_field)

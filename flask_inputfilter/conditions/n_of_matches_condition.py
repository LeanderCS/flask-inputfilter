from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class NOfMatchesCondition(BaseCondition):
    """
    Condition that ensures at least N of the specified
    fields matches the value.
    """

    __slots__ = ("fields", "n", "value")

    def __init__(self, fields: List[str], n: int, value: Any) -> None:
        self.fields = fields
        self.n = n
        self.value = value

    def check(self, data: Dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) == self.value)
            == self.n
        )

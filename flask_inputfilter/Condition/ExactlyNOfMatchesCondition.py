from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.Condition import BaseCondition


class ExactlyNOfMatchesCondition(BaseCondition):
    """
    Condition that checks if exactly n of the given fields
    match with the value.
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

from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class ExactlyNOfCondition(BaseCondition):
    """
    Condition that checks if exactly n of the given
    fields are present in the data.
    """

    __slots__ = ("fields", "n")

    def __init__(self, fields: List[str], n: int) -> None:
        self.fields = fields
        self.n = n

    def check(self, data: Dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) is not None)
            == self.n
        )

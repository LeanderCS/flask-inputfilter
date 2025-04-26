from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class ExactlyOneOfMatchesCondition(BaseCondition):
    """
    Condition that ensures exactly one of the specified
    fields matches the value.
    """

    __slots__ = ("fields", "value")

    def __init__(self, fields: List[str], value: Any) -> None:
        self.fields = fields
        self.value = value

    def check(self, data: Dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) == self.value)
            == 1
        )

from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class OneOfMatchesCondition(BaseCondition):
    """
    Condition that ensures at least one of the specified
    fields matches the value.
    """

    __slots__ = ("fields", "value")

    def __init__(self, fields: List[str], value: Any) -> None:
        self.fields = fields
        self.value = value

    def check(self, data: Dict[str, Any]) -> bool:
        return any(data.get(field) == self.value for field in self.fields)

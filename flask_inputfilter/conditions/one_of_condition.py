from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class OneOfCondition(BaseCondition):
    """
    Condition that ensures at least one of the specified fields is present.
    """

    __slots__ = ("fields",)

    def __init__(self, fields: List[str]) -> None:
        self.fields = fields

    def check(self, data: Dict[str, Any]) -> bool:
        return any(
            field in data and data.get(field) is not None
            for field in self.fields
        )

from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class ExactlyOneOfCondition(BaseCondition):
    """
    Condition that ensures exactly one of the specified fields is present.
    """

    __slots__ = ("fields",)

    def __init__(self, fields: List[str]) -> None:
        self.fields = fields

    def check(self, data: Dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) is not None) == 1
        )

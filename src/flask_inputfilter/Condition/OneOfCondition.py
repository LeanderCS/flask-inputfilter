from typing import Any, Dict, List

from .BaseCondition import BaseCondition


class OneOfCondition(BaseCondition):
    """
    Condition that ensures at least one of the specified fields is present.
    """

    def __init__(self, fields: List[str]) -> None:
        self.fields = fields

    def check(self, data: Dict[str, Any]) -> bool:
        return any(
            field in data and data.get(field) is not None
            for field in self.fields
        )

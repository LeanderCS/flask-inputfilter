from typing import Any, Dict, List

from .BaseCondition import BaseCondition


class ExactlyOneOfCondition(BaseCondition):
    """
    Condition that ensures exactly one of the specified fields is present.
    """

    def __init__(self, fields: List[str]) -> None:
        self.fields = fields

    def check(self, data: Dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) is not None) == 1
        )

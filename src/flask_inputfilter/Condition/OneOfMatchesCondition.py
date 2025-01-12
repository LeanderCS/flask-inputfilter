from typing import Any, Dict, List

from .BaseCondition import BaseCondition


class OneOfMatchesCondition(BaseCondition):
    """
    Condition that ensures at least one of the specified
    fields matches the value.
    """

    def __init__(self, fields: List[str], value: Any) -> None:

        self.fields = fields
        self.value = value

    def check(self, data: Dict[str, Any]) -> bool:

        return any(data.get(field) == self.value for field in self.fields)

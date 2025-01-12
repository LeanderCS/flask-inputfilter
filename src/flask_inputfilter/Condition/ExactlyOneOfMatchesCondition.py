from typing import Any, Dict, List

from .BaseCondition import BaseCondition


class ExactlyOneOfMatchesCondition(BaseCondition):
    """
    Condition that ensures exactly one of the specified fields matches the value.
    """

    def __init__(self, fields: List[str], value: Any) -> None:

        self.fields = fields
        self.value = value

    def check(self, data: Dict[str, Any]) -> bool:

        return (
            sum(1 for field in self.fields if data.get(field) == self.value)
            == 1
        )

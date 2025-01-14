from typing import Any, List

from .BaseCondition import BaseCondition


class NOfCondition(BaseCondition):
    """
    Condition that ensures at least N of the specified fields are present.
    """

    def __init__(self, fields: List[str], n: int) -> None:
        self.fields = fields
        self.n = n

    def check(self, data: Any) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) is not None)
            >= self.n
        )

from typing import Any, Dict

from .BaseCondition import BaseCondition


class EqualCondition(BaseCondition):
    """
    Condition that checks if two fields are equal.
    """

    def __init__(self, first_field: str, second_field: str) -> None:
        self.first_field = first_field
        self.second_field = second_field

    def check(self, data: Dict[str, Any]) -> bool:
        return data.get(self.first_field) == data.get(self.second_field)

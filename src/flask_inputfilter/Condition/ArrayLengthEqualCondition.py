from typing import Any, Dict

from .BaseCondition import BaseCondition


class ArrayLengthEqualCondition(BaseCondition):
    """
    Condition that checks if the array is of the specified length.
    """

    def __init__(self, first_field: str, second_field: str) -> None:

        self.first_field = first_field
        self.second_field = second_field

    def check(self, data: Dict[str, Any]) -> bool:

        return len(data.get(self.first_field) or []) == len(
            data.get(self.second_field) or []
        )

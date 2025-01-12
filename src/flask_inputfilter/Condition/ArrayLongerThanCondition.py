from typing import Any, Dict

from .BaseCondition import BaseCondition


class ArrayLongerThanCondition(BaseCondition):
    """
    Condition that checks if the array is longer than the specified length.
    """

    def __init__(self, longer_field: str, shorter_field: str) -> None:

        self.longer_field = longer_field
        self.shorter_field = shorter_field

    def check(self, data: Dict[str, Any]) -> bool:

        return len(data.get(self.longer_field) or []) > len(
            data.get(self.shorter_field) or []
        )

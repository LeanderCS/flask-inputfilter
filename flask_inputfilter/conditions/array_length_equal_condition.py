from __future__ import annotations

from typing import Any, Dict

from flask_inputfilter.conditions import BaseCondition


class ArrayLengthEqualCondition(BaseCondition):
    """
    Condition that checks if the array is of the specified length.
    """

    __slots__ = ("first_array_field", "second_array_field")

    def __init__(
        self, first_array_field: str, second_array_field: str
    ) -> None:
        self.first_array_field = first_array_field
        self.second_array_field = second_array_field

    def check(self, data: Dict[str, Any]) -> bool:
        return len(data.get(self.first_array_field) or []) == len(
            data.get(self.second_array_field) or []
        )

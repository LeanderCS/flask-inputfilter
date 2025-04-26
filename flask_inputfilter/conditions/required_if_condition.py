from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from flask_inputfilter.conditions import BaseCondition


class RequiredIfCondition(BaseCondition):
    """
    Condition that ensures a field is required if another
    field has a specific value.
    """

    __slots__ = ("condition_field", "value", "required_field")

    def __init__(
        self,
        condition_field: str,
        value: Optional[Union[Any, List[Any]]],
        required_field: str,
    ) -> None:
        self.condition_field = condition_field
        self.value = value
        self.required_field = required_field

    def check(self, data: Dict[str, Any]) -> bool:
        condition_value = data.get(self.condition_field)

        if self.value is not None:
            if isinstance(self.value, list):
                if condition_value in self.value:
                    return data.get(self.required_field) is not None
            else:
                if condition_value == self.value:
                    return data.get(self.required_field) is not None

        else:
            if condition_value is not None:
                return data.get(self.required_field) is not None

        return True

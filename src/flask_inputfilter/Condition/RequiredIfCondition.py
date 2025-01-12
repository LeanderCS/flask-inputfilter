from typing import Any, Dict

from .BaseCondition import BaseCondition


class RequiredIfCondition(BaseCondition):
    """
    Condition that ensures a field is required if another
    field has a specific value.
    """

    def __init__(
        self, condition_field: str, value: Any, required_field: str
    ) -> None:

        self.condition_field = condition_field
        self.value = value
        self.required_field = required_field

    def check(self, data: Dict[str, Any]) -> bool:

        return (
            data.get(self.condition_field) != self.value
            or data.get(self.required_field) is not None
        )

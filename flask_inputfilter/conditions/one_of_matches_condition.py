from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class OneOfMatchesCondition(BaseCondition):
    """
    Ensures that at least one of the specified fields matches a given value.

    **Parameters:**

    - **fields** (*list[str]*): A list of fields to check.
    - **value** (*Any*): The value to match against.

    **Expected Behavior:**

    Validates that at least one field from the specified list
    has the given value.

    **Example Usage:**

    .. code-block:: python

        class OneMatchRequiredFilter(InputFilter):
            option1 = field()

            option2 = field()

            condition(
                OneOfMatchesCondition(
                    fields=['option1', 'option2'],
                    value='yes'
                )
            )
    """

    __slots__ = ("fields", "value")

    def __init__(self, fields: list[str], value: Any) -> None:
        self.fields = fields
        self.value = value

    def check(self, data: dict[str, Any]) -> bool:
        return any(data.get(field) == self.value for field in self.fields)

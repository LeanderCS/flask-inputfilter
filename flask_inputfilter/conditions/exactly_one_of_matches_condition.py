from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class ExactlyOneOfMatchesCondition(BaseCondition):
    """
    Ensures that exactly one of the specified fields matches a given value.

    **Parameters:**

    - **fields** (*list[str]*): A list of fields to check.
    - **value** (*Any*): The value to match against.

    **Expected Behavior:**

    Validates that exactly one of the specified fields has the given value.

    **Example Usage:**

    .. code-block:: python

        class OneMatchFilter(InputFilter):
            option1 = field()

            option2 = field()

            condition(
                ExactlyOneOfMatchesCondition(
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
        return (
            sum(1 for field in self.fields if data.get(field) == self.value)
            == 1
        )

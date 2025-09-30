from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class ExactlyNOfMatchesCondition(BaseCondition):
    """
    Checks that exactly ``n`` of the specified fields match a given value.

    **Parameters:**

    - **fields** (*list[str]*): A list of fields to check.
    - **n** (*int*): The exact number of fields that must match the value.
    - **value** (*Any*): The value to match against.

    **Expected Behavior:**

    Validates that exactly ``n`` fields among the specified ones have the
    given value.

    **Example Usage:**

    .. code-block:: python

        class MatchFieldsFilter(InputFilter):
            field1 = field()

            field2 = field()

            condition(
                ExactlyNOfMatchesCondition(
                    fields=['field1', 'field2'],
                    n=1,
                    value='expected_value'
                )
            )
    """

    __slots__ = ("fields", "n", "value")

    def __init__(self, fields: list[str], n: int, value: Any) -> None:
        self.fields = fields
        self.n = n
        self.value = value

    def check(self, data: dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) == self.value)
            == self.n
        )

from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class NOfMatchesCondition(BaseCondition):
    """
    Checks that at least ``n`` of the specified fields match a given value.

    **Parameters:**

    - **fields** (*List[str]*): A list of fields to check.
    - **n** (*int*): The minimum number of fields that must match the value.
    - **value** (*Any*): The value to match against.

    **Expected Behavior:**

    Validates that the count of fields matching the given value is greater
    than or equal to ``n``.

    **Example Usage:**

    .. code-block:: python

        class MinimumMatchFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    'field1'
                )

                self.add(
                    'field2'
                )

                self.add_condition(
                    NOfMatchesCondition(
                        fields=['field1', 'field2'],
                        n=1,
                        value='value'
                    )
                )
    """

    __slots__ = ("fields", "n", "value")

    def __init__(self, fields: List[str], n: int, value: Any) -> None:
        self.fields = fields
        self.n = n
        self.value = value

    def check(self, data: Dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) == self.value)
            == self.n
        )

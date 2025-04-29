from __future__ import annotations

from typing import Any, List

from flask_inputfilter.conditions import BaseCondition


class NOfCondition(BaseCondition):
    """
    Checks that at least ``n`` of the specified fields are present in the input
    data.

    **Parameters:**

    - **fields** (*List[str]*): A list of fields to check.
    - **n** (*int*): The minimum number of fields that must be present.

    **Expected Behavior:**

    Validates that the count of the specified fields present is greater
    than or equal to ``n``.

    **Example Usage:**

    .. code-block:: python

        class MinimumFieldsFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    'field1'
                )

                self.add(
                    'field2'
                )

                self.add(
                    'field3'
                )

                self.add_condition(
                    NOfCondition(
                        fields=['field1', 'field2', 'field3'],
                        n=2
                    )
                )
    """

    __slots__ = ("fields", "n")

    def __init__(self, fields: List[str], n: int) -> None:
        self.fields = fields
        self.n = n

    def check(self, data: Any) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) is not None)
            >= self.n
        )

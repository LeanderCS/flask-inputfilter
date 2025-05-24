from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class ExactlyNOfCondition(BaseCondition):
    """
    Checks that exactly ``n`` of the specified fields are present in the input
    data.

    **Parameters:**

    - **fields** (*List[str]*): A list of fields to check.
    - **n** (*int*): The exact number of fields that must be present.

    **Expected Behavior:**

    Counts the number of specified fields present in the data and
    validates that the count equals ``n``.

    **Example Usage:**

    .. code-block:: python

        class ExactFieldsFilter(InputFilter):
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
                    ExactlyNOfCondition(
                        fields=['field1', 'field2', 'field3'],
                        n=2
                    )
                )
    """

    __slots__ = ("fields", "n")

    def __init__(self, fields: List[str], n: int) -> None:
        self.fields = fields
        self.n = n

    def check(self, data: Dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) is not None)
            == self.n
        )

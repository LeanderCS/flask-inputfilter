from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class ExactlyOneOfCondition(BaseCondition):
    """
    Ensures that exactly one of the specified fields is present.

    **Parameters:**

    - **fields** (*List[str]*): A list of fields to check.

    **Expected Behavior:**

    Validates that only one field among the specified fields exists in the
    input data.

    **Example Usage:**

    .. code-block:: python

        class OneFieldFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    'email'
                )

                self.add(
                    'phone'
                )

                self.add_condition(ExactlyOneOfCondition(['email', 'phone']))
    """

    __slots__ = ("fields",)

    def __init__(self, fields: List[str]) -> None:
        self.fields = fields

    def check(self, data: Dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) is not None) == 1
        )

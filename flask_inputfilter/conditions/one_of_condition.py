from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class OneOfCondition(BaseCondition):
    """
    Ensures that at least one of the specified fields is present in the input
    data.

    **Parameters:**

    - **fields** (*List[str]*): A list of fields to check.

    **Expected Behavior:**

    Validates that at least one field from the specified list is present.
    Fails if none are present.

    **Example Usage:**

    .. code-block:: python

        class OneFieldRequiredFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    'email'
                )

                self.add(
                    'phone'
                )

                self.add_condition(
                    OneOfCondition(
                        fields=['email', 'phone']
                    )
                )
    """

    __slots__ = ("fields",)

    def __init__(self, fields: List[str]) -> None:
        self.fields = fields

    def check(self, data: Dict[str, Any]) -> bool:
        return any(
            field in data and data.get(field) is not None
            for field in self.fields
        )

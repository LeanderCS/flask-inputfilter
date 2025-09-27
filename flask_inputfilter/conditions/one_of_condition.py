from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class OneOfCondition(BaseCondition):
    """
    Ensures that at least one of the specified fields is present in the input
    data.

    **Parameters:**

    - **fields** (*list[str]*): A list of fields to check.

    **Expected Behavior:**

    Validates that at least one field from the specified list is present.
    Fails if none are present.

    **Example Usage:**

    .. code-block:: python

        class OneFieldRequiredFilter(InputFilter):
            email: str = field()
            phone: str = field()

            condition(
                OneOfCondition(
                    fields=['email', 'phone']
                )
            )
    """

    __slots__ = ("fields",)

    def __init__(self, fields: list[str]) -> None:
        self.fields = fields

    def check(self, data: dict[str, Any]) -> bool:
        return any(
            field in data and data.get(field) is not None
            for field in self.fields
        )

from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class ExactlyOneOfCondition(BaseCondition):
    """
    Ensures that exactly one of the specified fields is present.

    **Parameters:**

    - **fields** (*list[str]*): A list of fields to check.

    **Expected Behavior:**

    Validates that only one field among the specified fields exists in the
    input data.

    **Example Usage:**

    .. code-block:: python

        class OneFieldFilter(InputFilter):
            email: str = field()
            phone: str = field()

            condition(ExactlyOneOfCondition(['email', 'phone']))
    """

    __slots__ = ("fields",)

    def __init__(self, fields: list[str]) -> None:
        self.fields = fields

    def check(self, data: dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) is not None) == 1
        )

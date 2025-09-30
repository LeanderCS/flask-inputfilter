from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class EqualCondition(BaseCondition):
    """
    Checks if two specified fields are equal.

    **Parameters:**

    - **first_field** (*str*): The first field to compare.
    - **second_field** (*str*): The second field to compare.

    **Expected Behavior:**

    Validates that the values of ``first_field`` and ``second_field`` are
    equal. Fails if they differ.

    **Example Usage:**

    .. code-block:: python

        class EqualFieldsFilter(InputFilter):
            password = field()

            confirm_password = field()

            condition(
                EqualCondition(
                    first_field='password',
                    second_field='confirm_password'
                )
            )
    """

    __slots__ = ("first_field", "second_field")

    def __init__(self, first_field: str, second_field: str) -> None:
        self.first_field = first_field
        self.second_field = second_field

    def check(self, data: dict[str, Any]) -> bool:
        return data.get(self.first_field) == data.get(self.second_field)

from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class ArrayLengthEqualCondition(BaseCondition):
    """
    Checks if two array fields have equal length.

    **Parameters:**

    - **first_array_field** (*str*): The first field containing an array.
    - **second_array_field** (*str*): The second field containing an array.

    **Expected Behavior:**

    Validates that the length of the array from ``first_array_field`` is
    equal to the length of the array from ``second_array_field``. If not,
    the condition fails.

    **Example Usage:**

    .. code-block:: python

        class ArrayLengthFilter(InputFilter):
            list1: list = field(validators=[IsArrayValidator()])
            list2: list = field(validators=[IsArrayValidator()])

            condition(
                ArrayLengthEqualCondition(
                    first_array_field='list1',
                    second_array_field='list2'
                )
            )
    """

    __slots__ = ("first_array_field", "second_array_field")

    def __init__(
        self, first_array_field: str, second_array_field: str
    ) -> None:
        self.first_array_field = first_array_field
        self.second_array_field = second_array_field

    def check(self, data: dict[str, Any]) -> bool:
        return len(data.get(self.first_array_field) or []) == len(
            data.get(self.second_array_field) or []
        )

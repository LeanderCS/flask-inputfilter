from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class ArrayLongerThanCondition(BaseCondition):
    """
    Checks if the array in one field is longer than the array in another field.

    **Parameters:**

    - **longer_field** (*str*): The field expected to have a longer array.
    - **shorter_field** (*str*): The field expected to have a shorter array.

    **Expected Behavior:**

    Validates that the array in ``longer_field`` has more elements than
    the array in ``shorter_field``.

    **Example Usage:**

    .. code-block:: python

        class ArrayComparisonFilter(InputFilter):
            list1 = field(
                validators=[IsArrayValidator()]
            )

            list2 = field(
                validators=[IsArrayValidator()]
            )

            condition(
                ArrayLongerThanCondition(
                    longer_field='list1',
                    shorter_field='list2'
                )
            )
    """

    __slots__ = ("longer_field", "shorter_field")

    def __init__(self, longer_field: str, shorter_field: str) -> None:
        self.longer_field = longer_field
        self.shorter_field = shorter_field

    def check(self, data: dict[str, Any]) -> bool:
        return len(data.get(self.longer_field) or []) > len(
            data.get(self.shorter_field) or []
        )

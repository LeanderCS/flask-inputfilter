from __future__ import annotations

from typing import Any, Dict

from flask_inputfilter.conditions import BaseCondition


class NotEqualCondition(BaseCondition):
    """
    Checks if two specified fields are not equal.

    **Parameters:**

    - **first_field** (*str*): The first field to compare.
    - **second_field** (*str*): The second field to compare.

    **Expected Behavior:**

    Validates that the values of ``first_field`` and ``second_field``
    are not equal.

    **Example Usage:**

    .. code-block:: python

        class DifferenceFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    'field1'
                )

                self.add(
                    'field2'
                )

                self.add_condition(NotEqualCondition('field1', 'field2'))
    """

    __slots__ = ("first_field", "second_field")

    def __init__(self, first_field: str, second_field: str) -> None:
        self.first_field = first_field
        self.second_field = second_field

    def check(self, data: Dict[str, Any]) -> bool:
        return data.get(self.first_field) != data.get(self.second_field)

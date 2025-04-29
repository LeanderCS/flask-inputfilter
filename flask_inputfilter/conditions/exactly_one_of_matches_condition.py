from __future__ import annotations

from typing import Any, Dict, List

from flask_inputfilter.conditions import BaseCondition


class ExactlyOneOfMatchesCondition(BaseCondition):
    """
    Ensures that exactly one of the specified fields matches a given value.

    **Parameters:**

    - **fields** (*List[str]*): A list of fields to check.
    - **value** (*Any*): The value to match against.

    **Expected Behavior:**

    Validates that exactly one of the specified fields has the given value.

    **Example Usage:**

    .. code-block:: python

        class OneMatchFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    'option1'
                )

                self.add(
                    'option2'
                )

                self.add_condition(
                    ExactlyOneOfMatchesCondition(
                        fields=['option1', 'option2'],
                        value='yes'
                    )
                )
    """

    __slots__ = ("fields", "value")

    def __init__(self, fields: List[str], value: Any) -> None:
        self.fields = fields
        self.value = value

    def check(self, data: Dict[str, Any]) -> bool:
        return (
            sum(1 for field in self.fields if data.get(field) == self.value)
            == 1
        )

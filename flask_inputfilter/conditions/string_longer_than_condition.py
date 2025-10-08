from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class StringLongerThanCondition(BaseCondition):
    """
    Checks if the length of the string in one field is longer than the string
    in another field.

    **Parameters:**

    - **longer_field** (*str*): The field expected to have a longer string.
    - **shorter_field** (*str*): The field expected to have a shorter string.

    **Expected Behavior:**

    Validates that the string in ``longer_field`` has a greater length
    than the string in ``shorter_field``.

    **Example Usage:**

    .. code-block:: python

        class StringLengthFilter(InputFilter):
            description: str = field()
            summary: str = field()

            condition(
                StringLongerThanCondition(
                    longer_field='description',
                    shorter_field='summary'
                )
            )
    """

    __slots__ = ("longer_field", "shorter_field")

    def __init__(self, longer_field: str, shorter_field: str) -> None:
        self.longer_field = longer_field
        self.shorter_field = shorter_field

    def check(self, data: dict[str, Any]) -> bool:
        return len(data.get(self.longer_field) or "") > len(
            data.get(self.shorter_field) or ""
        )

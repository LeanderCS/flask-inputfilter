from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseCondition


class IntegerBiggerThanCondition(BaseCondition):
    """
    Checks if the integer value in one field is greater than that in another
    field.

    **Parameters:**

    - **bigger_field** (*str*): The field expected to have a larger integer.
    - **smaller_field** (*str*): The field expected to have a smaller integer.

    **Expected Behavior:**

    Validates that the integer value from ``bigger_field`` is greater than
    the value from ``smaller_field``.

    **Example Usage:**

    .. code-block:: python

        class NumberComparisonFilter(InputFilter):
            field_should_be_bigger: int = field(
                validators=[IsIntegerValidator()]
            )

            field_should_be_smaller: int = field(
                validators=[IsIntegerValidator()]
            )

            condition(
                IntegerBiggerThanCondition(
                    bigger_field='field_should_be_bigger',
                    smaller_field='field_should_be_smaller'
                )
            )
    """

    __slots__ = ("bigger_field", "smaller_field")

    def __init__(self, bigger_field: str, smaller_field: str) -> None:
        self.bigger_field = bigger_field
        self.smaller_field = smaller_field

    def check(self, data: dict[str, Any]) -> bool:
        if (
            data.get(self.bigger_field) is None
            or data.get(self.smaller_field) is None
        ):
            return False

        return data.get(self.bigger_field) > data.get(self.smaller_field)

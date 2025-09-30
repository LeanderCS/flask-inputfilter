from __future__ import annotations

from typing import Any

from flask_inputfilter.helpers import parse_date
from flask_inputfilter.models import BaseCondition


class TemporalOrderCondition(BaseCondition):
    """
    Checks if one date is before another, ensuring the correct temporal order.
    Supports datetime objects, date objects, and ISO 8601 formatted strings.

    **Parameters:**

    - **smaller_date_field** (*str*): The field containing the earlier date.
    - **larger_date_field** (*str*): The field containing the later date.

    **Expected Behavior:**

    Validates that the date in ``smaller_date_field`` is earlier than the
    date in ``larger_date_field``. Raises a ``ValidationError`` if the
    dates are not in the correct order.

    **Example Usage:**

    .. code-block:: python

        class DateOrderFilter(InputFilter):
            start_date = field()

            end_date = field()

            condition(
                TemporalOrderCondition(
                    smaller_date_field='start_date',
                    larger_date_field='end_date'
                )
            )
    """

    __slots__ = ("larger_date_field", "smaller_date_field")

    def __init__(
        self, smaller_date_field: str, larger_date_field: str
    ) -> None:
        self.smaller_date_field = smaller_date_field
        self.larger_date_field = larger_date_field

    def check(self, data: dict[str, Any]) -> bool:
        return parse_date(data.get(self.smaller_date_field)) < parse_date(
            data.get(self.larger_date_field)
        )

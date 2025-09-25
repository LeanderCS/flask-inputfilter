from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToIntegerFilter(BaseFilter):
    """
    Converts the input value to an integer.

    **Expected Behavior:**

    - Attempts to cast the input using ``int()``.
    - On failure, returns the original value.

    **Example Usage:**

    .. code-block:: python

        class AgeFilter(InputFilter):
            age: int = field(filters=[
                ToIntegerFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[int, Any]:
        try:
            return int(value)

        except (ValueError, TypeError):
            return value

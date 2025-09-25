from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToFloatFilter(BaseFilter):
    """
    Converts the input value to a float.

    **Expected Behavior:**

    - Attempts to cast the input using ``float()``.
    - On a ValueError or TypeError, returns the original value.

    **Example Usage:**

    .. code-block:: python

        class PriceFilter(InputFilter):
            price: float = field(filters=[
                ToFloatFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[float, Any]:
        try:
            return float(value)

        except (ValueError, TypeError):
            return value

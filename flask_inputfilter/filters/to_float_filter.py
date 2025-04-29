from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToFloatFilter(BaseFilter):
    """
    Converts the input value to a float.

    **Expected Behavior:**

    - Attempts to cast the input using ``float()``.
    - On a ValueError or TypeError, returns the original value.

    **Example Usage:**

    .. code-block:: python

        class PriceFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('price', filters=[
                    ToFloatFilter()
                ])
    """

    def apply(self, value: Any) -> Union[float, Any]:
        try:
            return float(value)

        except (ValueError, TypeError):
            return value

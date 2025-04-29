from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToIntegerFilter(BaseFilter):
    """
    Converts the input value to an integer.

    **Expected Behavior:**

    - Attempts to cast the input using ``int()``.
    - On failure, returns the original value.

    **Example Usage:**

    .. code-block:: python

        class AgeFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('age', filters=[
                    ToIntegerFilter()
                ])
    """

    def apply(self, value: Any) -> Union[int, Any]:
        try:
            return int(value)

        except (ValueError, TypeError):
            return value

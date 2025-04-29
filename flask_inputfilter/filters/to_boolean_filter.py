from __future__ import annotations

from typing import Any, Optional, Union

from flask_inputfilter.filters import BaseFilter


class ToBooleanFilter(BaseFilter):
    """
    Converts the input value to a boolean.

    **Expected Behavior:**

    Uses Python's built-in ``bool()`` conversion. Note that non-empty
    strings and non-zero numbers will return ``True``.

    **Example Usage:**

    .. code-block:: python

        class ActiveFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('active', filters=[
                    ToBooleanFilter()
                ])
    """

    def apply(self, value: Any) -> Union[Optional[bool], Any]:
        return bool(value)

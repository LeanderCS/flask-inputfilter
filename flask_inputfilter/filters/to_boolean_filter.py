from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToBooleanFilter(BaseFilter):
    """
    Converts the input value to a boolean.

    **Expected Behavior:**

    Uses Python's built-in ``bool()`` conversion. Note that non-empty
    strings and non-zero numbers will return ``True``.

    **Example Usage:**

    .. code-block:: python

        class ActiveFilter(InputFilter):
            active: bool = field(filters=[
                ToBooleanFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[bool, Any]:
        return bool(value)

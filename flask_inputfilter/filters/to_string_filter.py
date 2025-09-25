from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToStringFilter(BaseFilter):
    """
    Converts any input value to its string representation.

    **Expected Behavior:**

    - Uses Python's built-in ``str()`` to convert the input to a string.

    **Example Usage:**

    .. code-block:: python

        class IdFilter(InputFilter):
            id: str = field(filters=[
                ToStringFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        return str(value)

from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToUpperFilter(BaseFilter):
    """
    Converts a string to uppercase.

    **Expected Behavior:**

    - For string inputs, returns the uppercase version.
    - Non-string inputs are returned unchanged.

    **Example Usage:**

    .. code-block:: python

        class CodeFilter(InputFilter):
            code: str = field(filters=[
                ToUpperFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        return value.upper()

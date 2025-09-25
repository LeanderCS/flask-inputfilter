from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToLowerFilter(BaseFilter):
    """
    Converts a string to lowercase.

    **Expected Behavior:**

    - For string inputs, returns the lowercase version.
    - Non-string inputs are returned unchanged.

    **Example Usage:**

    .. code-block:: python

        class UsernameFilter(InputFilter):
            username: str = field(filters=[
                ToLowerFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        return value.lower()

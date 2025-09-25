from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class TruncateFilter(BaseFilter):
    """
    Truncates a string to a specified maximum length.

    **Parameters:**

    - **max_length** (*int*): The maximum allowed length of the string.

    **Expected Behavior:**

    - If the string exceeds the specified length, it is truncated.
    - Non-string inputs are returned unchanged.

    **Example Usage:**

    .. code-block:: python

        class DescriptionFilter(InputFilter):
            description: str = field(filters=[
                TruncateFilter(max_length=100)
            ])
    """

    __slots__ = ("max_length",)

    def __init__(self, max_length: int) -> None:
        self.max_length = max_length

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        if len(value) > self.max_length:
            value = value[: self.max_length]

        return value

from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class TruncateFilter(BaseFilter):
    """
    Filter that truncates a string to a specified maximum length.
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

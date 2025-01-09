from typing import Any, Optional

from ..Filter.BaseFilter import BaseFilter


class TruncateFilter(BaseFilter):
    """
    Filter that truncates a string to a specified maximum length.
    """

    def __init__(self, max_length: int) -> None:

        self.max_length = max_length

    def apply(self, value: Any) -> Optional[str]:

        if not isinstance(value, str):
            return None

        if len(value) > self.max_length:
            value = value[: self.max_length]

        return value

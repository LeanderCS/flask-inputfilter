from typing import Any, Optional

from ..Filter.BaseFilter import BaseFilter


class ToIntegerFilter(BaseFilter):
    """
    Filter, that transforms the value to an Integer.
    """

    def apply(self, value: Any) -> Optional[int]:

        try:
            return int(value)

        except (ValueError, TypeError):
            return None

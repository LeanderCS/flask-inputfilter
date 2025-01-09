from typing import Any, Optional

from ..Filter.BaseFilter import BaseFilter


class ToBooleanFilter(BaseFilter):
    """
    Filter, that transforms the value to a boolean.
    """

    def apply(self, value: Any) -> Optional[bool]:

        try:
            return bool(value)

        except (ValueError, TypeError):
            return None

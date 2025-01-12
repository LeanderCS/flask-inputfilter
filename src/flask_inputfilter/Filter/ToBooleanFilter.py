from typing import Any, Optional, Union

from .BaseFilter import BaseFilter


class ToBooleanFilter(BaseFilter):
    """
    Filter, that transforms the value to a boolean.
    """

    def apply(self, value: Any) -> Union[Optional[bool], Any]:
        try:
            return bool(value)

        except (ValueError, TypeError):
            return value

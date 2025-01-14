from typing import Any, Union

from .BaseFilter import BaseFilter


class ToStringFilter(BaseFilter):
    """
    Filter, that transforms the value to a string.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        return str(value)

from typing import Any, Union

from .BaseFilter import BaseFilter


class StringTrimFilter(BaseFilter):
    """
    Filter, that removes leading and trailing whitespaces from a string.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        return value.strip() if isinstance(value, str) else value

from typing import Any, Union

from .BaseFilter import BaseFilter


class ToUpperFilter(BaseFilter):
    """
    Filter that converts a string to uppercase.
    """

    def apply(self, value: str) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        return value.upper()

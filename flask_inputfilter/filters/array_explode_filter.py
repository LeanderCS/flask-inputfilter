from __future__ import annotations

from typing import Any, List, Union

from flask_inputfilter.filters import BaseFilter


class ArrayExplodeFilter(BaseFilter):
    """
    Filter that splits a string into an array based on a specified delimiter.
    """

    __slots__ = ("delimiter",)

    def __init__(self, delimiter: str = ",") -> None:
        self.delimiter = delimiter

    def apply(self, value: Any) -> Union[List[str], Any]:
        if not isinstance(value, str):
            return value

        return value.split(self.delimiter)

from typing import Any, List, Optional

from ..Filter.BaseFilter import BaseFilter


class ArrayExplodeFilter(BaseFilter):
    """
    Filter that splits a string into an array based on a specified delimiter.
    """

    def __init__(self, delimiter: str = ",") -> None:

        self.delimiter = delimiter

    def apply(self, value: Any) -> Optional[List[str]]:

        if not isinstance(value, str):
            return None

        return value.split(self.delimiter)

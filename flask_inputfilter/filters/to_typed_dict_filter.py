from __future__ import annotations

from typing import Any

from flask_inputfilter.filters import BaseFilter


class ToTypedDictFilter(BaseFilter):
    """
    Filter that converts a dictionary to a TypedDict.
    """

    __slots__ = ("typed_dict",)

    def __init__(self, typed_dict) -> None:
        """
        Parameters:
            typed_dict (Type[TypedDict]): The TypedDict class
                to convert the dictionary to.
        """

        self.typed_dict = typed_dict

    def apply(self, value: Any) -> Any:
        if not isinstance(value, dict):
            return value

        return self.typed_dict(**value)

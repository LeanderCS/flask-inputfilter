from __future__ import annotations

from enum import Enum
from typing import Any, Type, Union

from flask_inputfilter.filters import BaseFilter


class ToEnumFilter(BaseFilter):
    """
    Filter that converts a value to an Enum instance.
    """

    __slots__ = ("enum_class",)

    def __init__(self, enum_class: Type[Enum]) -> None:
        self.enum_class = enum_class

    def apply(self, value: Any) -> Union[Enum, Any]:
        if not isinstance(value, (str, int)) or isinstance(value, Enum):
            return value

        try:
            return self.enum_class(value)

        except ValueError:
            return value

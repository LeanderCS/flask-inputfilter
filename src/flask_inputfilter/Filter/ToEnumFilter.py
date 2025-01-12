from enum import Enum
from typing import Any, Optional, Type

from .BaseFilter import BaseFilter


class ToEnumFilter(BaseFilter):
    """
    Filter that converts a value to an Enum instance.
    """

    def __init__(self, enum_class: Type[Enum]) -> None:

        self.enum_class = enum_class

    def apply(self, value: Any) -> Optional[Enum]:

        if not isinstance(value, (str, int)):
            return None

        try:
            return self.enum_class(value)

        except ValueError:
            return None

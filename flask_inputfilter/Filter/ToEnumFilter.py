from enum import Enum
from typing import Any, Type, Union

from flask_inputfilter.Filter import BaseFilter


class ToEnumFilter(BaseFilter):
    """
    Filter that converts a value to an Enum instance.
    """

    def __init__(self, enum_class: Type[Enum]) -> None:
        self.enum_class = enum_class

    def apply(self, value: Any) -> Union[Enum, Any]:
        if not isinstance(value, (str, int)):
            return value

        if isinstance(value, Enum):
            return value

        try:
            return self.enum_class(value)

        except ValueError:
            return value

from __future__ import annotations

from typing import Any, Type, Union

from flask_inputfilter.filters import BaseFilter


class ToDataclassFilter(BaseFilter):
    """
    Filter that converts a dictionary to a dataclass.
    """

    __slots__ = ("dataclass_type",)

    def __init__(self, dataclass_type: Type[dict]) -> None:
        self.dataclass_type = dataclass_type

    def apply(self, value: Any) -> Union[Any]:
        if not isinstance(value, dict):
            return value

        return self.dataclass_type(**value)

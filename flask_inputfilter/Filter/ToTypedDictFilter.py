from typing import Any, Type

from typing_extensions import TypedDict

from flask_inputfilter.Filter import BaseFilter


class ToTypedDictFilter(BaseFilter):
    """
    Filter that converts a dictionary to a TypedDict.
    """

    def __init__(self, typed_dict: Type[TypedDict]) -> None:
        self.typed_dict = typed_dict

    def apply(self, value: Any) -> Any:
        if not isinstance(value, dict):
            return value

        return self.typed_dict(**value)

from typing import Any, Type, Union

from flask_inputfilter.Filter import BaseFilter


class ToDataclassFilter(BaseFilter):
    """
    Filter that converts a dictionary to a dataclass.
    """

    def __init__(self, dataclass: Type[Any]) -> None:
        self.dataclass = dataclass

    def apply(self, value: Any) -> Union[Any]:
        if not isinstance(value, dict):
            return value

        return self.dataclass(**value)

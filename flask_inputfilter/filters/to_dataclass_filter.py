from __future__ import annotations

from typing import Any, Type

from flask_inputfilter.models import BaseFilter


class ToDataclassFilter(BaseFilter):
    """
    Converts a dictionary to a specified dataclass.

    **Parameters:**

    - **dataclass_type** (*Type[dict]*): The target dataclass type
      that the dictionary should be converted into.

    **Expected Behavior:**

    If the input is a dictionary, it instantiates the provided dataclass
    using the dictionary values. Otherwise, the input is returned unchanged.

    **Example Usage:**

    .. code-block:: python

        from my_dataclasses import MyDataClass

        class DataFilter(InputFilter):
            data = field(filters=[
                ToDataclassFilter(MyDataClass)
            ])
    """

    __slots__ = ("dataclass_type",)

    def __init__(self, dataclass_type: Type[dict]) -> None:
        self.dataclass_type = dataclass_type

    def apply(self, value: Any) -> Any:
        if not isinstance(value, dict):
            return value

        return self.dataclass_type(**value)

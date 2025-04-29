from __future__ import annotations

from enum import Enum
from typing import Any, Type, Union

from flask_inputfilter.filters import BaseFilter


class ToEnumFilter(BaseFilter):
    """
    Converts a value to an instance of a specified Enum.

    **Parameters:**

    - **enum_class** (*Type[Enum]*): The enum class to which the
        input should be converted.

    **Expected Behavior:**

    - If the input is a string or an integer, the filter attempts to
        convert it into the corresponding enum member.
    - If the input is already an enum instance, it is returned as is.
    - If conversion fails, the original input is returned.

    **Example Usage:**

    .. code-block:: python

        from my_enums import ColorEnum

        class ColorFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('color', filters=[
                    ToEnumFilter(ColorEnum)
                ])
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

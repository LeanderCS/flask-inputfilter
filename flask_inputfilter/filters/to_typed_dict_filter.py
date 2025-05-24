from __future__ import annotations

from typing import Any

from flask_inputfilter.filters import BaseFilter


class ToTypedDictFilter(BaseFilter):
    """
    Converts a dictionary into an instance of a specified TypedDict.

    **Parameters:**

    - **typed_dict** (*Type[TypedDict]*): The target TypedDict type.

    **Expected Behavior:**

    - If the input is a dictionary, returns an instance of the specified
        TypedDict.
    - Otherwise, returns the original value.

    **Example Usage:**

    .. code-block:: python

        class ConfigFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('config', filters=[
                    ToTypedDictFilter(MyTypedDict)
                ])
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

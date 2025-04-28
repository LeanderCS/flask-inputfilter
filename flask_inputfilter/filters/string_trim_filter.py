from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class StringTrimFilter(BaseFilter):
    """
    Removes leading and trailing whitespace from a string.

    **Expected Behavior:**

    If the input is a string, it returns the trimmed version. Otherwise,
    the value remains unchanged.

    **Example Usage:**

    .. code-block:: python

        class UserFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('username', filters=[
                    StringTrimFilter()
                ])
    """

    def apply(self, value: Any) -> Union[str, Any]:
        return value.strip() if isinstance(value, str) else value

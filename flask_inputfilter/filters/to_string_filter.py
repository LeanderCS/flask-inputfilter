from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToStringFilter(BaseFilter):
    """
    Converts any input value to its string representation.

    **Expected Behavior:**

    - Uses Python's built-in ``str()`` to convert the input to a string.

    **Example Usage:**

    .. code-block:: python

        class IdFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('id', filters=[
                    ToStringFilter()
                ])
    """

    def apply(self, value: Any) -> Union[str, Any]:
        return str(value)

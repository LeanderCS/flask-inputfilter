from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToUpperFilter(BaseFilter):
    """
    Converts a string to uppercase.

    **Expected Behavior:**

    - For string inputs, returns the uppercase version.
    - Non-string inputs are returned unchanged.

    **Example Usage:**

    .. code-block:: python

        class CodeFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('code', filters=[
                    ToUpperFilter()
                ])
    """

    def apply(self, value: str) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        return value.upper()

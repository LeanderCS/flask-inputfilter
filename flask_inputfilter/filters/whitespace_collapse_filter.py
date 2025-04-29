from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class WhitespaceCollapseFilter(BaseFilter):
    """
    Collapses multiple consecutive whitespace characters into a single space.

    **Expected Behavior:**

    - Replaces sequences of whitespace with a single space and trims
        the result.
    - Non-string inputs are returned unchanged.

    **Example Usage:**

    .. code-block:: python

        class AddressFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('address', filters=[
                    WhitespaceCollapseFilter()
                ])
    """

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"\s+", " ", value).strip()

        return value

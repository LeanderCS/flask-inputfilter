from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.models import BaseFilter


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
            address = field(filters=[
                WhitespaceCollapseFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        return re.sub(r"\s+", " ", value).strip()

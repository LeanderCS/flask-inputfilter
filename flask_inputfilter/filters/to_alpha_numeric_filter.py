from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToAlphaNumericFilter(BaseFilter):
    """
    Ensures that a string contains only alphanumeric characters by removing all
    non-word characters.

    **Expected Behavior:**

    Strips out any character that is not a letter, digit, or underscore
    from the input string.

    **Example Usage:**

    .. code-block:: python

        class CodeFilter(InputFilter):
            code = field(filters=[
                ToAlphaNumericFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        return re.sub(r"[^\w]", "", value)

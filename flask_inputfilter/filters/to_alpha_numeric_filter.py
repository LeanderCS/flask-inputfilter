from __future__ import annotations

import re
from typing import Any, Optional, Union

from flask_inputfilter.filters import BaseFilter


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
            def __init__(self):
                super().__init__()

                self.add('code', filters=[
                    ToAlphaNumericFilter()
                ])
    """

    def apply(self, value: Any) -> Union[Optional[str], Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"[^\w]", "", value)

        return value

import re
from typing import Any, Optional

from ..Filter.BaseFilter import BaseFilter


class ToAlphaNumericFilter(BaseFilter):
    """
    Filter that ensures a string contains only alphanumeric characters.
    """

    def apply(self, value: Any) -> Optional[str]:

        if not isinstance(value, str):
            return None

        value = re.sub(r"[^\w]", "", value)

        return value

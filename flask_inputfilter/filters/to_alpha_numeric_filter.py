from __future__ import annotations

import re
from typing import Any, Optional, Union

from flask_inputfilter.filters import BaseFilter


class ToAlphaNumericFilter(BaseFilter):
    """
    Filter that ensures a string contains only alphanumeric characters.
    """

    def apply(self, value: Any) -> Union[Optional[str], Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"[^\w]", "", value)

        return value

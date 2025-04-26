from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToUpperFilter(BaseFilter):
    """
    Filter that converts a string to uppercase.
    """

    def apply(self, value: str) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        return value.upper()

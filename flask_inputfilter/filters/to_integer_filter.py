from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToIntegerFilter(BaseFilter):
    """
    Filter, that transforms the value to an Integer.
    """

    def apply(self, value: Any) -> Union[int, Any]:
        try:
            return int(value)

        except (ValueError, TypeError):
            return value

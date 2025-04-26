from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToStringFilter(BaseFilter):
    """
    Filter, that transforms the value to a string.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        return str(value)

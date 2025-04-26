from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class StringTrimFilter(BaseFilter):
    """
    Filter, that removes leading and trailing whitespaces from a string.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        return value.strip() if isinstance(value, str) else value

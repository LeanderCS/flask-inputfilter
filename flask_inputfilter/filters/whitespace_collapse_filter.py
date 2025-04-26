from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class WhitespaceCollapseFilter(BaseFilter):
    """
    Filter that collapses multiple consecutive whitespace
    characters into a single space.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"\s+", " ", value).strip()

        return value

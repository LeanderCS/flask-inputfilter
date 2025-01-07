import re
from typing import Any, Optional

from ..Filter.BaseFilter import BaseFilter


class WhitespaceCollapseFilter(BaseFilter):
    """
    Filter that collapses multiple consecutive whitespace characters into a single space.
    """

    def apply(self, value: Any) -> Optional[str]:

        if not isinstance(value, str):
            return None

        value = re.sub(r"\s+", " ", value).strip()

        return value

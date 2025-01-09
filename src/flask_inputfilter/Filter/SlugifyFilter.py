import re
from typing import Any, Optional

from ..Filter.BaseFilter import BaseFilter


class SlugifyFilter(BaseFilter):
    """
    Filter that converts a string to a slug.
    """

    def apply(self, value: Any) -> Optional[str]:

        if not isinstance(value, str):
            return None

        value = value.lower()

        value = re.sub(r"[^\w\s-]", "", value)
        value = re.sub(r"[\s]+", "-", value)

        return value

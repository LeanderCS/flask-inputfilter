import re
from typing import Any, Optional

from ..Filter.BaseFilter import BaseFilter


class ToPascaleCaseFilter(BaseFilter):
    """
    Filter that converts a string to PascalCase.
    """

    def apply(self, value: Any) -> Optional[str]:

        if not isinstance(value, str):
            return None

        value = re.sub(r"[\s\-_]+", " ", value).strip()

        value = "".join(word.capitalize() for word in value.split())

        return value

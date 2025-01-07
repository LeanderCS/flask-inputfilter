import re
from typing import Any, Optional

from ..Filter.BaseFilter import BaseFilter


class ToSnakeCaseFilter(BaseFilter):
    """
    Filter that converts a string to snake_case.
    """

    def apply(self, value: Any) -> Optional[str]:

        if not isinstance(value, str):
            return None

        value = re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()

        value = re.sub(r"[\s-]+", "_", value)

        return value

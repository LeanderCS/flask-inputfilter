from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToSnakeCaseFilter(BaseFilter):
    """
    Filter that converts a string to snake_case.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()
        value = re.sub(r"[\s-]+", "_", value)

        return value

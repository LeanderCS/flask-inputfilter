from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.filters import BaseFilter


class ToCamelCaseFilter(BaseFilter):
    """
    Filter that converts a string to camelCase.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"[\s_-]+", " ", value).strip()
        value = "".join(word.capitalize() for word in value.split())

        return value[0].lower() + value[1:] if value else value

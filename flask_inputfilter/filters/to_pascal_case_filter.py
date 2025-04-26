from __future__ import annotations

import re
from typing import Any, Optional, Union

from flask_inputfilter.filters import BaseFilter


class ToPascalCaseFilter(BaseFilter):
    """
    Filter that converts a string to PascalCase.
    """

    def apply(self, value: Any) -> Union[Optional[str], Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"[\s\-_]+", " ", value).strip()

        value = "".join(word.capitalize() for word in value.split())

        return value

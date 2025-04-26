from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.filters import BaseFilter


class ToDigitsFilter(BaseFilter):
    """
    Filter that converts a string to its corresponding digit type.
    """

    def apply(self, value: Any) -> Union[float, int, Any]:
        if not isinstance(value, str):
            return value

        elif re.fullmatch(RegexEnum.INTEGER_PATTERN.value, value):
            return int(value)

        elif re.fullmatch(RegexEnum.FLOAT_PATTERN.value, value):
            return float(value)

        return value

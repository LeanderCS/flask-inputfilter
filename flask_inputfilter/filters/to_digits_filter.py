from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.models import BaseFilter


class ToDigitsFilter(BaseFilter):
    """
    Converts a string to a numeric type (either an integer or a float).

    **Expected Behavior:**

    - If the input string matches an integer pattern, it returns an integer.
    - If it matches a float pattern, it returns a float.
    - Otherwise, the input is returned unchanged.

    **Example Usage:**

    .. code-block:: python

        class QuantityFilter(InputFilter):
            quantity = field(filters=[
                ToDigitsFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[float, int, Any]:
        if not isinstance(value, str):
            return value

        if re.fullmatch(RegexEnum.INTEGER_PATTERN.value, value):
            return int(value)

        if re.fullmatch(RegexEnum.FLOAT_PATTERN.value, value):
            return float(value)

        return value

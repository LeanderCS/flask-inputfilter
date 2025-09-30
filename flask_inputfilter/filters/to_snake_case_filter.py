from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToSnakeCaseFilter(BaseFilter):
    """
    Converts a string to snake_case.

    **Expected Behavior:**

    - Inserts underscores before uppercase letters (except the first),
      converts the string to lowercase, and replaces spaces or hyphens
      with underscores.
    - Non-string inputs are returned unchanged.

    **Example Usage:**

    .. code-block:: python

        class VariableFilter(InputFilter):
            variableName = field(filters=[
                ToSnakeCaseFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()
        return re.sub(r"[\s-]+", "_", value)

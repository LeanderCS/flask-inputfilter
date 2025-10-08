from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToPascalCaseFilter(BaseFilter):
    """
    Converts a string to PascalCase.

    **Expected Behavior:**

    - Capitalizes the first letter of each word and concatenates
      them without spaces.
    - Returns non-string inputs unchanged.

    **Example Usage:**

    .. code-block:: python

        class ClassNameFilter(InputFilter):
            class_name = field(filters=[
                ToPascalCaseFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"[\s\-_]+", " ", value).strip()

        return "".join(word.capitalize() for word in value.split())

from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ToCamelCaseFilter(BaseFilter):
    """
    Transforms a string into camelCase format.

    **Expected Behavior:**

    Normalizes delimiters such as spaces, underscores, or hyphens,
    capitalizes each word (except the first), and concatenates them
    so that the first letter is lowercase.

    **Example Usage:**

    .. code-block:: python

        class IdentifierFilter(InputFilter):
            identifier: str = field(filters=[
                ToCamelCaseFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"[\s_-]+", " ", value).strip()
        value = "".join(word.capitalize() for word in value.split())

        return value[0].lower() + value[1:] if value else value

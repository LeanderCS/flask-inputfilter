import re
from typing import Any, Optional, Union

from .BaseFilter import BaseFilter


class ToCamelCaseFilter(BaseFilter):
    """
    Filter that converts a string to camelCase.
    """

    def apply(self, value: Any) -> Union[Optional[str], Any]:
        if not isinstance(value, str):
            return value

        value = re.sub(r"[\s_-]+", " ", value).strip()

        value = "".join(word.capitalize() for word in value.split())

        return value[0].lower() + value[1:] if value else value

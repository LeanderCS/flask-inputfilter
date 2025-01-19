import re
from typing import Any, Optional, Union

from flask_inputfilter.Filter import BaseFilter


class SlugifyFilter(BaseFilter):
    """
    Filter that converts a string to a slug.
    """

    def apply(self, value: Any) -> Union[Optional[str], Any]:
        if not isinstance(value, str):
            return value

        value = value.lower()

        value = re.sub(r"[^\w\s-]", "", value)
        value = re.sub(r"[\s]+", "-", value)

        return value

from __future__ import annotations

import re
import unicodedata
from typing import Any, Optional, Union

from flask_inputfilter.enums import UnicodeFormEnum
from flask_inputfilter.filters import BaseFilter


class StringSlugifyFilter(BaseFilter):
    """
    Filter that converts a string to a slug.
    """

    def apply(self, value: Any) -> Union[Optional[str], Any]:
        if not isinstance(value, str):
            return value

        value_without_accents = "".join(
            char
            for char in unicodedata.normalize(UnicodeFormEnum.NFD.value, value)
            if unicodedata.category(char) != "Mn"
        )

        value = unicodedata.normalize(
            UnicodeFormEnum.NFKD.value, value_without_accents
        )
        value = value.encode("ascii", "ignore").decode("ascii")

        value = value.lower()

        value = re.sub(r"[^\w\s-]", "", value)
        value = re.sub(r"[\s]+", "-", value)

        return value

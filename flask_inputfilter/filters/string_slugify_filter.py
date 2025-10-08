from __future__ import annotations

import re
import unicodedata
from typing import Any, Union

from flask_inputfilter.enums import UnicodeFormEnum
from flask_inputfilter.models import BaseFilter


class StringSlugifyFilter(BaseFilter):
    """
    Converts a string into a slug format.

    **Expected Behavior:**

    Normalizes Unicode, converts to ASCII, lowercases the string,
    and replaces spaces with hyphens, producing a URL-friendly slug.

    **Example Usage:**

    .. code-block:: python

        class PostFilter(InputFilter):
            title = field(filters=[
                StringSlugifyFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        value_without_accents = "".join(
            char
            for char in unicodedata.normalize(
                UnicodeFormEnum.NFD.value,
                value,
            )
            if unicodedata.category(char) != "Mn"
        )

        value = unicodedata.normalize(
            UnicodeFormEnum.NFKD.value,
            value_without_accents,
        )
        value = value.encode("ascii", "ignore").decode("ascii")

        value = value.lower()

        value = re.sub(r"[^\w\s-]", "", value)
        return re.sub(r"[\s]+", "-", value)

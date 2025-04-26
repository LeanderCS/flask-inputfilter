from __future__ import annotations

import unicodedata
from typing import Any, Union

from flask_inputfilter.enums import UnicodeFormEnum
from flask_inputfilter.filters import BaseFilter


class ToNormalizedUnicodeFilter(BaseFilter):
    """
    Filter that normalizes a string to a specified Unicode form.
    """

    __slots__ = ("form",)

    def __init__(
        self,
        form: UnicodeFormEnum = UnicodeFormEnum.NFC,
    ) -> None:
        if not isinstance(form, UnicodeFormEnum):
            form = UnicodeFormEnum(form)

        self.form = form

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        value_without_accents = "".join(
            char
            for char in unicodedata.normalize(UnicodeFormEnum.NFD.value, value)
            if unicodedata.category(char) != "Mn"
        )

        return unicodedata.normalize(self.form.value, value_without_accents)

import unicodedata
from typing import Any, Optional

from typing_extensions import Literal

from ..Filter.BaseFilter import BaseFilter


class ToNormalizedUnicodeFilter(BaseFilter):
    """
    Filter that normalizes a string to a specified Unicode form.
    """

    def __init__(
        self, form: Literal["NFC", "NFD", "NFKC", "NFKD"] = "NFC"
    ) -> None:

        self.form = form

    def apply(self, value: Any) -> Optional[str]:

        if not isinstance(value, str):
            return None

        value = unicodedata.normalize(self.form, value)

        value_without_accents = "".join(
            char
            for char in unicodedata.normalize("NFD", value)
            if unicodedata.category(char) != "Mn"
        )

        return unicodedata.normalize(self.form, value_without_accents)

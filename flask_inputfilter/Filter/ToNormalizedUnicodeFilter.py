import unicodedata
from typing import Any, Union

from typing_extensions import Literal

from flask_inputfilter.Enum import UnicodeFormEnum
from flask_inputfilter.Filter import BaseFilter


class ToNormalizedUnicodeFilter(BaseFilter):
    """
    Filter that normalizes a string to a specified Unicode form.
    """

    def __init__(
        self,
        form: Union[
            UnicodeFormEnum, Literal["NFC", "NFD", "NFKC", "NFKD"]
        ] = UnicodeFormEnum.NFC,
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

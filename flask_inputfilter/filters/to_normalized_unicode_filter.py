from __future__ import annotations

import unicodedata
from typing import Any, Union

from flask_inputfilter.enums import UnicodeFormEnum
from flask_inputfilter.filters import BaseFilter


class ToNormalizedUnicodeFilter(BaseFilter):
    """
    Normalizes a Unicode string to a specified form.

    **Parameters:**

    - **form** (
            *Union[UnicodeFormEnum,
            Literal["NFC", "NFD", "NFKC", "NFKD"]]*,
            default: ``UnicodeFormEnum.NFC``
        ): The target Unicode normalization form.

    **Expected Behavior:**

    - Removes accent characters and normalizes the string based on the
        specified form.
    - Returns non-string inputs unchanged.

    **Example Usage:**

    .. code-block:: python

        class TextFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('text', filters=[
                    ToNormalizedUnicodeFilter(form="NFKC")
                ])
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

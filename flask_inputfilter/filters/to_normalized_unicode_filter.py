from __future__ import annotations

import unicodedata
import warnings
from typing import Any, Optional, Union

from flask_inputfilter.enums import UnicodeFormEnum
from flask_inputfilter.models import BaseFilter


class ToNormalizedUnicodeFilter(BaseFilter):
    """
    Normalizes a Unicode string to a specified form.

    **Parameters:**

    - **form** (*UnicodeFormEnum*, default: ``UnicodeFormEnum.NFC``):
      The target Unicode normalization form.

    **Expected Behavior:**

    - Removes accent characters and normalizes the string based on the
      specified form.
    - Returns non-string inputs unchanged.

    **Example Usage:**

    .. code-block:: python

        class TextFilter(InputFilter):
            text = field(filters=[
                ToNormalizedUnicodeFilter(form=UnicodeFormEnum.NFKC)
            ])
    """

    __slots__ = ("form",)

    def __init__(
        self,
        form: Optional[UnicodeFormEnum] = None,
    ) -> None:
        if form and not isinstance(form, UnicodeFormEnum):
            warnings.warn(
                "Directly using a sting is deprecated, use UnicodeFormEnum "
                "instead",
                DeprecationWarning,
                stacklevel=2,
            )
            form = UnicodeFormEnum(form)

        self.form = form if form else UnicodeFormEnum.NFC

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

        return unicodedata.normalize(
            self.form.value,
            value_without_accents,
        )

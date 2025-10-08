from __future__ import annotations

import re
from typing import Any, Union

from flask_inputfilter.models import BaseFilter

emoji_pattern = (
    r"["
    "\U0001f600-\U0001f64f"
    "\U0001f300-\U0001f5ff"
    "\U0001f680-\U0001f6ff"
    "\U0001f1e0-\U0001f1ff"
    "\U00002702-\U000027b0"
    "\U000024c2-\U0001f251"
    "]+"
)


class StringRemoveEmojisFilter(BaseFilter):
    """
    Removes emojis from a string using regular expression matching.

    **Expected Behavior:**

    If the input is a string, all emoji characters are removed;
    non-string inputs are returned unchanged.

    **Example Usage:**

    .. code-block:: python

        class CommentFilter(InputFilter):
            comment = field(filters=[
                StringRemoveEmojisFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        return re.sub(emoji_pattern, "", value)

import re
from typing import Any

from .BaseFilter import BaseFilter

emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)


class RemoveEmojisFilter(BaseFilter):
    """
    Filter that removes emojis from a string.
    """

    def apply(self, value: Any) -> str:

        if not isinstance(value, str):
            return value

        return emoji_pattern.sub("", value)

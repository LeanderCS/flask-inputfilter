from __future__ import annotations

from typing import Any

from flask_inputfilter.models import BaseFilter


class BlacklistFilter(BaseFilter):
    """
    Filters out unwanted substrings or keys based on a predefined blacklist.

    **Parameters:**

    - **blacklist** (*list[str]*): A list of substrings (for strings) or keys
      (for dictionaries) that should be removed.

    **Expected Behavior:**

    - For strings: Removes any occurrence of blacklisted items and trims
      whitespace.
    - For lists: Filters out items present in the blacklist.
    - For dictionaries: Removes key-value pairs where the key is blacklisted.

    **Example Usage:**

    .. code-block:: python

        class CommentFilter(InputFilter):
            comment: str = field(filters=[
                BlacklistFilter(blacklist=["badword1", "badword2"])
            ])
    """

    __slots__ = ("blacklist",)

    def __init__(self, blacklist: list[str]) -> None:
        self.blacklist = blacklist

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            for item in self.blacklist:
                value = value.replace(item, "")
            return value.strip()

        if isinstance(value, list):
            return [item for item in value if item not in self.blacklist]

        if isinstance(value, dict):
            return {
                key: value
                for key, value in value.items()
                if key not in self.blacklist
            }

        return value

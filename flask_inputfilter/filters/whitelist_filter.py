from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.models import BaseFilter


class WhitelistFilter(BaseFilter):
    """
    Filters the input by only keeping elements that appear in a predefined
    whitelist.

    **Parameters:**

    - **whitelist** (*list[str]*, optional): A list of allowed words
      or keys. If not provided, no filtering is applied.

    **Expected Behavior:**

    - For strings: Splits the input by whitespace and returns only
      the words present in the whitelist.
    - For lists: Returns a list of items that are in the whitelist.
    - For dictionaries: Returns a dictionary containing only the
       whitelisted keys.

    **Example Usage:**

    .. code-block:: python

        class RolesFilter(InputFilter):
            roles: list = field(filters=[
                WhitelistFilter(whitelist=["admin", "user"])
            ])
    """

    __slots__ = ("whitelist",)

    def __init__(self, whitelist: Optional[list[str]] = None) -> None:
        self.whitelist = whitelist

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            return " ".join(
                [word for word in value.split() if word in self.whitelist]
            )

        if isinstance(value, list):
            return [item for item in value if item in self.whitelist]

        if isinstance(value, dict):
            return {
                key: value
                for key, value in value.items()
                if key in self.whitelist
            }

        return value

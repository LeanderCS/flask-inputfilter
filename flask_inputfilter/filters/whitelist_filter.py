from __future__ import annotations

from typing import Any, List

from flask_inputfilter.filters import BaseFilter


class WhitelistFilter(BaseFilter):
    """
    Filters the input by only keeping elements that appear in a predefined
    whitelist.

    **Parameters:**

    - **whitelist** (*List[str]*, optional): A list of allowed words
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
            def __init__(self):
                super().__init__()

                self.add('roles', filters=[
                    WhitelistFilter(whitelist=["admin", "user"])
                ])
    """

    __slots__ = ("whitelist",)

    def __init__(self, whitelist: List[str] = None) -> None:
        self.whitelist = whitelist

    def apply(self, value: Any) -> Any:
        if isinstance(value, str):
            return " ".join(
                [word for word in value.split() if word in self.whitelist]
            )

        elif isinstance(value, list):
            return [item for item in value if item in self.whitelist]

        elif isinstance(value, dict):
            return {
                key: value
                for key, value in value.items()
                if key in self.whitelist
            }

        return value

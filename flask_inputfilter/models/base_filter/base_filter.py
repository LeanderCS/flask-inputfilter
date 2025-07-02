from __future__ import annotations

from typing import Any


class BaseFilter:
    """
    BaseFilter-Class.

    Every filter should inherit from it.
    """

    def apply(self, value: Any) -> Any:
        raise NotImplementedError(
            "The apply method must be implemented in filters."
        )

from __future__ import annotations

from abc import ABC
from typing import Any


class BaseFilter(ABC):
    """
    BaseFilter-Class.

    Every filter should inherit from it.
    """

    def apply(self, value: Any) -> Any:
        raise NotImplementedError(
            "The apply method must be implemented in filters."
        )

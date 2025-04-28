from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseFilter(ABC):
    """
    BaseFilter-Class.

    Every filter should inherit from it.
    """

    @abstractmethod
    def apply(self, value: Any) -> Any:
        pass

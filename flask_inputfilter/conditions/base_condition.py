from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseCondition(ABC):
    """
    Base class for defining conditions.

    Each condition should implement the `check` method.
    """

    @abstractmethod
    def check(self, data: Dict[str, Any]) -> bool:
        pass

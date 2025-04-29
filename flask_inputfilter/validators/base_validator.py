from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseValidator(ABC):
    """
    BaseValidator-Class.

    Every validator should inherit from it.
    """

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass

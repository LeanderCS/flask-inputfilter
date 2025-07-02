from __future__ import annotations

from typing import Any


class BaseCondition:
    """
    Base class for defining conditions.

    Each condition should implement the `check` method.
    """

    def check(self, data: dict[str, Any]) -> bool:
        raise NotImplementedError(
            "The check method must be implemented in conditions."
        )

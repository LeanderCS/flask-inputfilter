from typing import Any, Dict


class BaseCondition:
    """
    Base class for defining conditions.
    Each condition should implement the `check` method.
    """

    def check(self, data: Dict[str, Any]) -> bool:
        raise NotImplementedError("Condition must implement 'check' method.")

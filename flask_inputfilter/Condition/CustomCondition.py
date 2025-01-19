from typing import Any, Callable, Dict

from flask_inputfilter.Condition import BaseCondition


class CustomCondition(BaseCondition):
    """
    Allows users to define their own condition as a callable.
    """

    def __init__(self, condition: Callable[[Dict[str, Any]], bool]) -> None:
        self.condition = condition

    def check(self, data: Dict[str, Any]) -> bool:
        return self.condition(data)

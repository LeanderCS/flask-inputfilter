from __future__ import annotations

from typing import Any, Callable, Dict

from flask_inputfilter.Condition import BaseCondition


class CustomCondition(BaseCondition):
    """
    Allows users to define their own condition as a callable.
    """

    __slots__ = ("condition",)

    def __init__(self, condition: Callable[[Dict[str, Any]], bool]) -> None:
        self.condition = condition

    def check(self, data: Dict[str, Any]) -> bool:
        return self.condition(data)

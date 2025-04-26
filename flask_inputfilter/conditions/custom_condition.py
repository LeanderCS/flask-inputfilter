from __future__ import annotations

from collections.abc import Callable
from typing import Any, Dict

from flask_inputfilter.conditions import BaseCondition


class CustomCondition(BaseCondition):
    """
    Allows users to define their own condition as a callable.
    """

    __slots__ = ("condition",)

    def __init__(self, condition: Callable[[Dict[str, Any]], bool]) -> None:
        self.condition = condition

    def check(self, data: Dict[str, Any]) -> bool:
        return self.condition(data)

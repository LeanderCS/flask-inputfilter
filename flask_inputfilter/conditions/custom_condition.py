from __future__ import annotations

from collections.abc import Callable
from typing import Any, Dict

from flask_inputfilter.conditions import BaseCondition


class CustomCondition(BaseCondition):
    """
    Allows defining a custom condition using a user-provided callable.

    **Parameters:**

    - **condition** (*Callable[[Dict[str, Any]], bool]*): A function that
        takes the input data and returns a boolean indicating whether the
        condition is met.

    **Expected Behavior:**

    Executes the provided callable with the input data. The condition passes
    if the callable returns ``True``, and fails otherwise.

    **Example Usage:**

    .. code-block:: python

        def my_custom_condition(data):
            return data.get('age', 0) >= 18

        class CustomFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    'age',
                    validators=[IsIntegerValidator()]
                )

                self.add_condition(
                    CustomCondition(
                        condition=my_custom_condition
                    )
                )
    """

    __slots__ = ("condition",)

    def __init__(self, condition: Callable[[Dict[str, Any]], bool]) -> None:
        self.condition = condition

    def check(self, data: Dict[str, Any]) -> bool:
        return self.condition(data)

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flask_inputfilter.models import BaseCondition

if TYPE_CHECKING:
    from collections.abc import Callable


class CustomCondition(BaseCondition):
    """
    Allows defining a custom condition using a user-provided callable.

    **Parameters:**

    - **condition** (*Callable[[dict[str, Any]], bool]*): A function that
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
            age: int = field(validators=[IsIntegerValidator()])

            condition(
                CustomCondition(
                    condition=my_custom_condition
                )
            )
    """

    __slots__ = ("condition",)

    def __init__(self, condition: Callable[[dict[str, Any]], bool]) -> None:
        self.condition = condition

    def check(self, data: dict[str, Any]) -> bool:
        return self.condition(data)

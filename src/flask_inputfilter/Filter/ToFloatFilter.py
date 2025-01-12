from typing import Any, Union

from .BaseFilter import BaseFilter


class ToFloatFilter(BaseFilter):
    """
    Filter that converts a value to a float.
    """

    def apply(self, value: Any) -> Union[float, Any]:
        try:
            return float(value)

        except (ValueError, TypeError):
            return value

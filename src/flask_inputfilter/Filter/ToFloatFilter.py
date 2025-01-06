from ..Filter.BaseFilter import BaseFilter


class ToFloatFilter(BaseFilter):
    """
    Filter that converts a value to a float.
    """

    def apply(self, value: str) -> float:

        return float(value)

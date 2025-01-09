from ..Filter.BaseFilter import BaseFilter


class ToUpperFilter(BaseFilter):
    """
    Filter that converts a string to uppercase.
    """

    def apply(self, value: str) -> str:

        return value.upper()

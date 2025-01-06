from ..Filter.BaseFilter import BaseFilter


class ToLowerFilter(BaseFilter):
    """
    Filter that converts a string to lowercase.
    """

    def apply(self, value: str) -> str:

        return value.lower()

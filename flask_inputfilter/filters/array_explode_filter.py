from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ArrayExplodeFilter(BaseFilter):
    """
    Splits a string into an array based on a specified delimiter.

    **Parameters:**

    - **delimiter** (*str*, default: ``","``): The delimiter used to split
      the string.

    **Expected Behavior:**

    If the input value is a string, it returns a list of substrings. For
    non-string values, it returns the value unchanged.

    **Example Usage:**

    .. code-block:: python

        class TagFilter(InputFilter):
            tags = field(filters=[
                ArrayExplodeFilter(delimiter=";")
            ])
    """

    __slots__ = ("delimiter",)

    def __init__(self, delimiter: str = ",") -> None:
        self.delimiter = delimiter

    def apply(self, value: Any) -> Union[list[str], Any]:
        if not isinstance(value, str):
            return value

        return value.split(self.delimiter)

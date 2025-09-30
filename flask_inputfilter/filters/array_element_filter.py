from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.models import BaseFilter


class ArrayElementFilter(BaseFilter):
    """
    Filters each element in an array by applying one or more `BaseFilter`

    **Parameters:**

    - **element_filter** (*BaseFilter* | *list[BaseFilter]*): A filter or a
      list of filters to apply to each element in the array.

    **Expected Behavior:**

    Validates that the input is a list and applies the specified filter(s) to
    each element. If any element does not conform to the expected structure,
    a `ValueError` is raised.

    **Example Usage:**

    .. code-block:: python

        class TagInputFilter(InputFilter):
            tags = field(filters=[
                ArrayElementFilter(element_filter=StringTrimFilter())
            ])
    """

    __slots__ = ("element_filter",)

    def __init__(
        self,
        element_filter: Union[BaseFilter, list[BaseFilter]],
    ) -> None:
        self.element_filter = element_filter

    def apply(self, value: Any) -> list[Any]:
        if not isinstance(value, list):
            return value

        result = []
        for element in value:
            if isinstance(self.element_filter, BaseFilter):
                result.append(self.element_filter.apply(element))
                continue

            if isinstance(self.element_filter, list) and all(
                isinstance(v, BaseFilter) for v in self.element_filter
            ):
                for filter_instance in self.element_filter:
                    element = filter_instance.apply(element)
                result.append(element)
                continue

            result.append(element)
        return result

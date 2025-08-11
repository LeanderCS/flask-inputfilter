from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator

if TYPE_CHECKING:
    from flask_inputfilter.models import BaseFilter


class LazyFilterChain:
    """
    A lazy evaluation wrapper for filter chains that delays processing until
    needed.

    This can significantly improve performance when dealing with large filter
    chains or when early filters might invalidate the need for later
    processing.
    """

    __slots__ = ("_filters", "_processed", "_result", "_value")

    def __init__(self, filters: list[BaseFilter], value: Any) -> None:
        self._filters = filters
        self._value = value
        self._processed = False
        self._result = None

    def _process(self) -> Generator[Any, None, None]:
        """Generator that lazily applies filters."""
        current_value = self._value
        for filter in self._filters:
            if current_value is None:
                yield None
                return
            current_value = filter.apply(current_value)
            yield current_value

    def get_result(self) -> Any:
        """Get the final result, processing filters only when needed."""
        if not self._processed:
            # Process all filters and get the final result
            for result in self._process():
                self._result = result
            self._processed = True
        return self._result

    def apply_until(self, condition: callable) -> Any:
        """
        Apply filters until a condition is met.

        This allows for early termination of filter processing.
        """
        current_value = self._value
        for filter in self._filters:
            if current_value is None or condition(current_value):
                return current_value
            current_value = filter.apply(current_value)
        return current_value

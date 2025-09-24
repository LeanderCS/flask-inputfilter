# cython: language=c++
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False

from typing import Any


cdef class BaseCondition:
    """
    Base class for defining conditions.

    Each condition should implement the `check` method.
    """

    cpdef bint check(self, dict[str, Any] data):
        """
        Check if the condition is met based on the provided data.

        Args:
            data: Dictionary containing the data to validate against.

        Returns:
            True if the condition is satisfied, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the check method") from None

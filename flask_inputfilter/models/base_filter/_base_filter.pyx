# cython: language=c++
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False


cdef class BaseFilter:
    """
    BaseFilter-Class.

    Every filter should inherit from it.
    """

    cpdef object apply(self, object value):
        """
        Apply the filter to the given value.

        Args:
            value: The value to apply the filter to.

        Returns:
            The filtered value.

        Raises:
            NotImplementedError: If the method is not implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the apply method") from None

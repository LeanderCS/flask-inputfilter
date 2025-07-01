# cython: language=c++

cdef class BaseFilter:
    """
    BaseFilter-Class.

    Every filter should inherit from it.
    """

    cpdef object apply(self, object value):
        """
        Apply the filter to the given value.

        This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the apply method")

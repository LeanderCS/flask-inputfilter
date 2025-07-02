# cython: language=c++

cdef class BaseValidator:
    """
    BaseValidator-Class.

    Every validator should inherit from it.
    """

    cpdef void validate(self, object value) except *:
        """
        Validate the given value.

        Args:
            value: The value to validate.

        Raises:
            ValidationError: If the value is invalid.
            NotImplementedError: If the method is not implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the validate method") 
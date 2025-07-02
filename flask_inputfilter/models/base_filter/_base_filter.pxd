cdef class BaseFilter:
    cpdef object apply(self, object value)

cdef class BaseValidator:
    cpdef void validate(self, object value) except * 
from typing import Any


cdef class BaseCondition:
    cpdef bint check(self, dict[str, Any] data) 
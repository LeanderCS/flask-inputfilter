# cython: language=c++
# cython: freelist=256

import cython


cdef list EMPTY_LIST = []


@cython.final
cdef class FieldModel:
    """
    FieldModel is a dataclass that represents a field in the input data.
    """

    cdef public bint required
    cdef public object _default
    cdef public object fallback
    cdef public list filters
    cdef public list validators
    cdef public list steps
    cdef public object external_api
    cdef public str copy

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    def __init__(
        self,
        bint required = False,
        object default = None,
        object fallback = None,
        list filters = None,
        list validators = None,
        list steps = None,
        object external_api = None,
        str copy = None
    ) -> None:
        self.required = required
        self._default = default
        self.fallback = fallback
        self.filters = filters if filters is not None else EMPTY_LIST
        self.validators = validators if validators is not None else EMPTY_LIST
        self.steps = steps if steps is not None else EMPTY_LIST
        self.external_api = external_api
        self.copy = copy

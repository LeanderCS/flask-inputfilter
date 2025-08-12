# cython: language=c++
# cython: freelist=1024
# cython: boundscheck=False
# cython: wraparound=False
# cython: nonecheck=False
# cython: initializedcheck=False
# cython: overflowcheck=False

import cython
from typing import Any

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, ExternalApiConfig

cdef list EMPTY_LIST = []
cdef tuple EMPTY_TUPLE = ()


@cython.final
cdef class FieldModel:
    """
    FieldModel is a dataclass that represents a field in the input data.
    """

    @property
    def default(self) -> Any:
        return self._default

    @default.setter
    def default(self, value: Any) -> None:
        self._default = value

    def __init__(
        self,
        bint required=False,
        object default=None,
        object fallback=None,
        list[BaseFilter] filters=None,
        list[BaseValidator] validators=None,
        list steps=None,
        ExternalApiConfig external_api=None,
        str copy=None
    ) -> None:
        self.required = required
        self._default = default
        self.fallback = fallback
        self.filters = EMPTY_LIST if filters is None or len(filters) == 0 else filters
        self.validators = EMPTY_LIST if validators is None or len(validators) == 0 else validators
        self.steps = EMPTY_LIST if steps is None or len(steps) == 0 else steps
        self.external_api = external_api
        self.copy = copy

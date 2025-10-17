# cython: language=c++
# cython: freelist=1024
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: overflowcheck=False
# cython: initializedcheck=False
# cython: nonecheck=False

import cython
from typing import Any

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, ExternalApiConfig

cdef list EMPTY_LIST = []

cdef list[BaseFilter] _empty_filters = []
cdef list[BaseValidator] _empty_validators = []
cdef list _empty_steps = []


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
        str copy=None,
        object computed=None,
        object input_filter=None
    ) -> None:
        self.required = required
        self._default = default
        self.fallback = fallback

        if filters is not None and len(filters) > 0:
            self.filters = filters
        else:
            self.filters = _empty_filters

        if validators is not None and len(validators) > 0:
            self.validators = validators
        else:
            self.validators = _empty_validators

        if steps is not None and len(steps) > 0:
            self.steps = steps
        else:
            self.steps = _empty_steps

        self.external_api = external_api
        self.copy = copy
        self.computed = computed
        self.input_filter = input_filter

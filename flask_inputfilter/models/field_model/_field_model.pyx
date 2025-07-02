# cython: language=c++
# cython: freelist=256

import cython
from typing import Any

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, ExternalApiConfig

cdef list EMPTY_LIST = []


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
        self.filters = filters if filters is not None else EMPTY_LIST
        self.validators = validators if validators is not None else EMPTY_LIST
        self.steps = steps if steps is not None else EMPTY_LIST
        self.external_api = external_api
        self.copy = copy

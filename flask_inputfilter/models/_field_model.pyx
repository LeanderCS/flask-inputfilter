# cython: language=c++
# cython: language_level=3
# cython: binding=True
# cython: cdivision=True
# cython: boundscheck=False
# cython: initializedcheck=False
from __future__ import annotations

from typing import Any, List, Optional, Union

from flask_inputfilter.filters import BaseFilter
from flask_inputfilter.models import ExternalApiConfig
from flask_inputfilter.validators import BaseValidator


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
        required: bool = False,
        default: Any = None,
        fallback: Any = None,
        filters: List[BaseFilter] = None,
        validators: List[BaseValidator] = None,
        steps: List[Union[BaseFilter, BaseValidator]] = None,
        external_api: Optional[ExternalApiConfig] = None,
        copy: Optional[str] = None
    ) -> None:
        self.required = required
        self.default = default
        self.fallback = fallback
        self.filters = filters or []
        self.validators = validators or []
        self.steps = steps or []
        self.external_api = external_api
        self.copy = copy

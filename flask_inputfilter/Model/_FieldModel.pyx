from __future__ import annotations

from dataclasses import field
from typing import Any, List, Optional, Union

from flask_inputfilter.Filter import BaseFilter
from flask_inputfilter.Model import ExternalApiConfig
from flask_inputfilter.Validator import BaseValidator


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
        if filters is not None:
            self.filters = filters
        if validators is not None:
            self.validators = validators
        if steps is not None:
            self.steps = steps
        self.external_api = external_api
        self.copy = copy

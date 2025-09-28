# cython: language=c++

from typing import Any

from flask_inputfilter.models.cimports cimport BaseCondition, BaseFilter, BaseValidator, ExternalApiConfig, FieldModel

from libcpp.vector cimport vector
from libcpp.string cimport string


cdef extern from "helper.h":
    vector[string] make_default_methods()


cdef class InputFilter:
    cdef readonly:
        vector[string] methods
        dict[str, FieldModel] fields
        list[BaseCondition] conditions
        list[BaseFilter] global_filters
        list[BaseValidator] global_validators
        dict[str, Any] data
        dict[str, Any] validated_data
        dict[str, str] errors
        object model_class

    cpdef bint is_valid(self)
    cpdef object validate_data(self, dict data=*)
    cpdef void add_condition(self, BaseCondition condition)
    cpdef list get_conditions(self)
    cpdef void set_data(self, dict data)
    cpdef object get_value(self, str name)
    cpdef dict get_values(self)
    cpdef object get_raw_value(self, str name)
    cpdef dict get_raw_values(self)
    cpdef dict get_unfiltered_data(self)
    cpdef void set_unfiltered_data(self, dict data)
    cpdef bint has_unknown(self)
    cpdef str get_error_message(self, str field_name)
    cpdef dict get_error_messages(self)
    cpdef void add(
        self,
        str name,
        bint required=*,
        object default=*,
        object fallback=*,
        list[BaseFilter] filters=*,
        list[BaseValidator] validators=*,
        list steps=*,
        ExternalApiConfig external_api=*,
        str copy=*,
    ) except*
    cpdef bint has(self, str field_name)
    cpdef FieldModel get_input(self, str field_name)
    cpdef dict get_inputs(self)
    cpdef object remove(self, str field_name)
    cpdef int count(self)
    cpdef void replace(
        self,
        str name,
        bint required=*,
        object default=*,
        object fallback=*,
        list[BaseFilter] filters=*,
        list[BaseValidator] validators=*,
        list steps=*,
        ExternalApiConfig external_api=*,
        str copy=*,
    )
    cpdef void add_global_filter(self, BaseFilter filter)
    cpdef list get_global_filters(self)
    cpdef void clear(self)
    cpdef void merge(self, InputFilter other)
    cpdef void set_model(self, object model_class)
    cpdef void add_global_validator(self, BaseValidator validator)
    cpdef list[BaseValidator] get_global_validators(self)
    cdef object _serialize(self)
    cdef void _set_methods(self, list methods)
    cdef void _register_decorator_components(self)

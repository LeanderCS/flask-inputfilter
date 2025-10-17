# cython: language_level=3

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, ExternalApiConfig

cdef class FieldDescriptor:
    cdef readonly:
        bint required
        object _default
        object fallback
        list[BaseFilter] filters
        list[BaseValidator] validators
        list[BaseFilter | BaseValidator] steps
        ExternalApiConfig external_api
        str copy
        object computed
        object input_filter

    cdef public:
        str name

    cpdef void __set_name__(self, object owner, str name)

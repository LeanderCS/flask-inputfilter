# cython: language_level=3

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, ExternalApiConfig

cdef class FieldDescriptor:
    cdef readonly:
        bint required
        object _default
        object fallback
        list[BaseFilter] filters
        list[BaseValidator] validators
        list steps
        ExternalApiConfig external_api
        str copy
    cdef public:
        str name

    cpdef void __set_name__(self, object owner, str name)

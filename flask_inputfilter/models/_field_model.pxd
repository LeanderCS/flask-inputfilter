from flask_inputfilter.models._base_filter cimport BaseFilter


cdef class FieldModel:
    cdef public:
        bint required
        object _default
        object fallback
        list[BaseFilter] filters
        list validators
        list steps
        object external_api
        str copy

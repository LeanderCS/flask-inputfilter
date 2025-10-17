from flask_inputfilter.models.cimports cimport BaseValidator, BaseFilter, ExternalApiConfig


cdef class FieldModel:
    cdef public:
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

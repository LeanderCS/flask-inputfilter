cdef class FieldModel:
    cdef public:
        bint required
        object _default
        object fallback
        list filters
        list validators
        list steps
        object external_api
        str copy

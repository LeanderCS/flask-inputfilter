cdef class ExternalApiConfig:
    cdef public:
        str url
        str method
        dict params
        str data_key
        str api_key
        dict headers

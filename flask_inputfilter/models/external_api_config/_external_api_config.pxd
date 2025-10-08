from typing import Any


cdef class ExternalApiConfig:
    cdef public:
        str url
        str method
        dict[str, Any] params
        str data_key
        str api_key
        dict[str, str] headers
        int timeout

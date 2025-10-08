from typing import Any


cdef class ExternalApiConfig:
    cdef public:
        str url
        str method
        dict[str, Any] params
        str data_key
        str api_key
        dict[str, str] headers
        bint async_mode
        int timeout
        int retry_count
        double retry_delay

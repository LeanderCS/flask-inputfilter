# cython: language=c++
# cython: freelist=256
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False

import cython
from typing import Any


@cython.final
cdef class ExternalApiConfig:
    """
    Configuration for an external API call.

    **Parameters:**

    - **url** (*str*): The URL of the external API.
    - **method** (*str*): The HTTP method to use.
    - **params** (*Optional[dict[str, Any]]*): The parameters to send to
      the API.
    - **data_key** (*Optional[str]*): The key in the response JSON to use
    - **api_key** (*Optional[str]*): The API key to use.
    - **headers** (*Optional[dict[str, str]]*): The headers to send to the API.
    - **async_mode** (*bool*): Whether to use async HTTP client (httpx).
      Default: False.
    - **timeout** (*int*): Timeout in seconds for the HTTP request.
      Default: 30.
    - **retry_count** (*int*): Number of retry attempts on failure.
      Default: 0.
    - **retry_delay** (*float*): Delay in seconds between retries.
      Default: 1.0.
    """

    def __init__(
        self,
        str url,
        str method,
        dict[str, Any] params=None,
        str data_key=None,
        str api_key=None,
        dict[str, str] headers=None,
        bint async_mode=False,
        int timeout=30,
        int retry_count=0,
        double retry_delay=1.0
    ) -> None:
        self.url = url
        self.method = method
        self.params = params
        self.data_key = data_key
        self.api_key = api_key
        self.headers = headers
        self.async_mode = async_mode
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay

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
    - **timeout** (*int*): The timeout in seconds for the API request.
    """

    def __init__(
        self,
        str url,
        str method,
        dict[str, Any] params=None,
        str data_key=None,
        str api_key=None,
        dict[str, str] headers=None,
        int timeout = 30
    ) -> None:
        self.url = url
        self.method = method
        self.params = params
        self.data_key = data_key
        self.api_key = api_key
        self.headers = headers
        self.timeout = timeout

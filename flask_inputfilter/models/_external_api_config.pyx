# cython: language=c++
# cython: freelist=256

import cython


@cython.final
cdef class ExternalApiConfig:
    """
    Configuration for an external API call.

    **Parameters:**

    - **url** (*str*): The URL of the external API.
    - **method** (*str*): The HTTP method to use.
    - **params** (*Optional[dict[str, str]]*): The parameters to send to
      the API.
    - **data_key** (*Optional[str]*): The key in the response JSON to use
    - **api_key** (*Optional[str]*): The API key to use.
    - **headers** (*Optional[dict[str, str]]*): The headers to send to the API.
    """

    def __init__(
        self,
        str url,
        str method,
        dict params = None,
        str data_key = None,
        str api_key = None,
        dict headers = None
    ) -> None:
        self.url = url
        self.method = method
        self.params = params
        self.data_key = data_key
        self.api_key = api_key
        self.headers = headers

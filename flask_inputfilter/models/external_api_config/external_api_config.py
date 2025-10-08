from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExternalApiConfig:
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
    - **timeout** (*int*): The timeout in seconds for the API request.
    """

    url: str
    method: str
    params: Optional[dict[str, str]] = None
    data_key: Optional[str] = None
    api_key: Optional[str] = None
    headers: Optional[dict[str, str]] = None
    timeout: int = 30

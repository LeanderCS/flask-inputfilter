from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ExternalApiConfig:
    """
    Configuration for an external API call.

    :param url: The URL of the external API.
    :param method: The HTTP method to use.
    :param params: The parameters to send to the API.
    :param data_key: The key in the response JSON to use
    :param api_key: The API key to use.
    :param headers: The headers to send to the API.
    """

    url: str
    method: str
    params: Optional[Dict[str, str]] = None
    data_key: Optional[str] = None
    api_key: Optional[str] = None
    headers: Optional[Dict[str, str]] = None

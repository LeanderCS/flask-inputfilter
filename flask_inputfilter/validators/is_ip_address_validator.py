from __future__ import annotations

import ipaddress
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsIpAddressValidator(BaseValidator):
    """
    Checks if a value is a valid IP address. Supports IPv4 and IPv6.

    **Parameters:**

    - **version** (*Optional[int]*): Restricts the check to a specific IP
      version. Allowed values are ``4`` and ``6``. If not set, both
      versions are accepted.
    - **error_message** (*Optional[str]*): Custom error message if the
      value is not a valid IP address.

    **Expected Behavior:**

    Ensures the input is a string that parses as an IP address of the
    requested version. Raises a ``ValidationError`` if the value is not
    a valid IP address.

    **Example Usage:**

    .. code-block:: python

        class NetworkInputFilter(InputFilter):
            client_ip: str = field(validators=[
                IsIpAddressValidator(version=4)
            ])
    """

    __slots__ = ("error_message", "version")

    def __init__(
        self,
        version: Optional[int] = None,
        error_message: Optional[str] = None,
    ) -> None:
        if version not in (None, 4, 6):
            raise ValueError("version must be 4, 6 or None.")

        self.version = version
        self.error_message = error_message or (
            f"Value is not a valid IPv{version} address."
            if version
            else "Value is not a valid IP address."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")

        try:
            address = ipaddress.ip_address(value)
        except ValueError:
            raise ValidationError(self.error_message) from None

        if self.version is not None and address.version != self.version:
            raise ValidationError(self.error_message)

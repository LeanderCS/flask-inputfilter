"""IP address validator for IPv4 and IPv6 addresses."""

from __future__ import annotations

import ipaddress
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsIpAddressValidator(BaseValidator):
    """
    Validates IP addresses (IPv4 and IPv6).

    This validator checks if a value is a valid IP address and can optionally
    validate specific IP versions and types.
    """

    def __init__(
        self,
        version: Optional[int] = None,
        allow_private: bool = True,
        allow_loopback: bool = True,
        allow_multicast: bool = True,
        allow_link_local: bool = True,
        allow_reserved: bool = True,
        allow_ipv6_mapped: bool = True,
        require_cidr: bool = False,
        allow_network: bool = True,
    ) -> None:
        """
        Initialize the IP address validator.

        Args:
            version: IP version (4 or 6), None for both
            allow_private: Whether to allow private IP addresses
            allow_loopback: Whether to allow loopback addresses
            allow_multicast: Whether to allow multicast addresses
            allow_link_local: Whether to allow link-local addresses
            allow_reserved: Whether to allow reserved addresses
            allow_ipv6_mapped: Whether to allow IPv6-mapped IPv4 addresses
            require_cidr: Whether to require CIDR notation
            allow_network: Whether to allow network addresses
        """
        self.version = version
        self.allow_private = allow_private
        self.allow_loopback = allow_loopback
        self.allow_multicast = allow_multicast
        self.allow_link_local = allow_link_local
        self.allow_reserved = allow_reserved
        self.allow_ipv6_mapped = allow_ipv6_mapped
        self.require_cidr = require_cidr
        self.allow_network = allow_network

    def validate(self, value: Any) -> None:
        """
        Validate the IP address.

        Args:
            value: The value to validate

        Raises:
            ValidationError: If the value is not a valid IP address
        """
        if value is None:
            raise ValidationError("IP address cannot be None")

        if not isinstance(value, str):
            raise ValidationError(
                f"IP address must be a string, not {type(value).__name__}"
            )

        try:
            if "/" in value or self.require_cidr:
                ip = ipaddress.ip_network(value, strict=not self.allow_network)
                if self.require_cidr and "/" not in value:
                    raise ValidationError("CIDR notation is required")
            else:
                ip = ipaddress.ip_address(value)
        except ValueError as e:
            raise ValidationError(f"Invalid IP address: {e!s}")

        if self.version is not None and ip.version != self.version:
            raise ValidationError(
                f"IP version {ip.version} not allowed, expected IPv{self.version}"
            )

        if isinstance(ip, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
            self._validate_network(ip)
        else:
            self._validate_address(ip)

    def _validate_address(self, ip: ipaddress.ip_address) -> None:
        """Validate a single IP address."""
        if not self.allow_private and ip.is_private:
            raise ValidationError(
                f"Private IP addresses are not allowed: {ip}"
            )

        if not self.allow_loopback and ip.is_loopback:
            raise ValidationError(f"Loopback addresses are not allowed: {ip}")

        if not self.allow_multicast and ip.is_multicast:
            raise ValidationError(f"Multicast addresses are not allowed: {ip}")

        if not self.allow_link_local and ip.is_link_local:
            raise ValidationError(
                f"Link-local addresses are not allowed: {ip}"
            )

        if not self.allow_reserved and ip.is_reserved:
            raise ValidationError(f"Reserved addresses are not allowed: {ip}")

        if (
            isinstance(ip, ipaddress.IPv6Address)
            and not self.allow_ipv6_mapped
            and ip.ipv4_mapped
        ):
            raise ValidationError(
                f"IPv6-mapped IPv4 addresses are not allowed: {ip}"
            )

    def _validate_network(self, network: ipaddress.ip_network) -> None:
        """Validate a network address."""
        self._validate_address(network.network_address)

        if network.num_addresses == 1:
            self._validate_address(
                next(iter(network.hosts()))
                if network.hosts()
                else network.network_address
            )

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar, Optional, Union

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class FileSizeValidator(BaseValidator):
    """
    Validates file sizes against specified limits.

    This validator checks if file sizes are within acceptable ranges, useful
    for file upload validation.
    """

    SIZE_UNITS: ClassVar = {
        "B": 1,
        "KB": 1024,
        "MB": 1024 * 1024,
        "GB": 1024 * 1024 * 1024,
        "TB": 1024 * 1024 * 1024 * 1024,
    }

    def __init__(
        self,
        max_size: Optional[Union[int, str]] = None,
        min_size: Optional[Union[int, str]] = None,
        exact_size: Optional[Union[int, str]] = None,
        allow_empty: bool = False,
        human_readable: bool = True,
    ) -> None:
        """
        Initialize the file size validator.

        Args:
            max_size: Maximum file size (bytes or string like "10MB")
            min_size: Minimum file size (bytes or string like "1KB")
            exact_size: Exact file size required
            allow_empty: Whether to allow empty files (0 bytes)
            human_readable: Whether to show human-readable sizes in errors

        Examples:
            FileSizeValidator(max_size="10MB")
            FileSizeValidator(max_size=10485760)  # 10MB in bytes
            FileSizeValidator(min_size="1KB", max_size="100MB")
        """
        self.max_size = self._parse_size(max_size) if max_size else None
        self.min_size = self._parse_size(min_size) if min_size else None
        self.exact_size = self._parse_size(exact_size) if exact_size else None
        self.allow_empty = allow_empty
        self.human_readable = human_readable

    def validate(self, value: Any) -> None:
        """
        Validate the file size.

        Args:
            value: Can be:
                - File path (string)
                - File object with 'size' attribute
                - Dictionary with 'size' key
                - Integer representing size in bytes
                - Werkzeug FileStorage object

        Raises:
            ValidationError: If the file size is invalid
        """
        size = self._get_file_size(value)

        if size == 0 and not self.allow_empty:
            raise ValidationError("Empty files are not allowed")

        if self.exact_size is not None and size != self.exact_size:
            raise ValidationError(
                f"File size must be exactly {self._format_size(self.exact_size)}, "
                f"got {self._format_size(size)}"
            )

        if self.min_size is not None and size < self.min_size:
            raise ValidationError(
                f"File size must be at least {self._format_size(self.min_size)}, "
                f"got {self._format_size(size)}"
            )

        if self.max_size is not None and size > self.max_size:
            raise ValidationError(
                f"File size must not exceed {self._format_size(self.max_size)}, "
                f"got {self._format_size(size)}"
            )

    def _get_file_size(self, value: Any) -> int:
        """
        Extract file size from various input types.

        Args:
            value: The input value

        Returns:
            File size in bytes

        Raises:
            ValidationError: If file size cannot be determined
        """
        if value is None:
            raise ValidationError("File cannot be None")

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            if Path(value).is_file():
                return Path(value).stat().st_size
            try:
                return self._parse_size(value)
            except (ValueError, TypeError):
                raise ValidationError(f"File not found: {value}")

        if isinstance(value, dict):
            if "size" in value:
                return int(value["size"])
            if "content_length" in value:
                return int(value["content_length"])
            raise ValidationError(
                "Dictionary must have 'size' or 'content_length' key"
            )

        if hasattr(value, "size"):
            return int(value.size)

        if (
            hasattr(value, "content_length")
            and value.content_length is not None
        ):
            return int(value.content_length)

        if hasattr(value, "read") and hasattr(value, "seek"):
            try:
                current = value.tell()
                value.seek(0, 2)
                size = value.tell()
                value.seek(current)
                return size
            except OSError:
                pass

        if isinstance(value, (bytes, bytearray)):
            return len(value)

        raise ValidationError(
            f"Cannot determine file size from {type(value).__name__}"
        )

    def _parse_size(self, size: Union[int, str]) -> int:
        """
        Parse size string to bytes.

        Args:
            size: Size as integer (bytes) or string (e.g., "10MB")

        Returns:
            Size in bytes

        Raises:
            ValueError: If size string is invalid
        """
        if isinstance(size, int):
            return size

        if not isinstance(size, str):
            raise ValueError(
                f"Size must be int or str, not {type(size).__name__}"
            )

        size = size.strip().upper()

        import re

        match = re.match(r"^(\d+(?:\.\d+)?)\s*([KMGT]?B)?$", size)

        if not match:
            raise ValueError(f"Invalid size format: {size}")

        number = float(match.group(1))
        unit = match.group(2) or "B"

        if unit not in self.SIZE_UNITS:
            raise ValueError(f"Invalid size unit: {unit}")

        return int(number * self.SIZE_UNITS[unit])

    def _format_size(self, size: int) -> str:
        """
        Format size in human-readable format.

        Args:
            size: Size in bytes

        Returns:
            Formatted size string
        """
        if not self.human_readable:
            return f"{size} bytes"

        for unit in ["TB", "GB", "MB", "KB"]:
            unit_size = self.SIZE_UNITS[unit]
            if size >= unit_size:
                return f"{size / unit_size:.2f} {unit}"

        return f"{size} bytes"

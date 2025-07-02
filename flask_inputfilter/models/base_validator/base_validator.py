from __future__ import annotations

from typing import Any


class BaseValidator:
    """
    BaseValidator-Class.

    Every validator should inherit from it.
    """

    def validate(self, value: Any) -> None:
        raise NotImplementedError(
            "The validate method must be implemented in validators."
        )

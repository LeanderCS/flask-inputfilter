from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.models import BaseFilter


class ToNullFilter(BaseFilter):
    """
    Transforms the input to ``None`` if it is an empty string or already
    ``None``.

    **Expected Behavior:**

    - If the input is ``""`` or ``None``, returns ``None``.
    - Otherwise, returns the original value.

    **Example Usage:**

    .. code-block:: python

        class MiddleNameFilter(InputFilter):
            middle_name = field(filters=[
                ToNullFilter()
            ])
    """

    __slots__ = ()

    def apply(self, value: Any) -> Optional[Any]:
        return None if value in ("", None) else value

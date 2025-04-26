from __future__ import annotations

from typing import Any, Optional, Union

from flask_inputfilter.filters import BaseFilter


class ToBooleanFilter(BaseFilter):
    """
    Filter, that transforms the value to a boolean.
    """

    def apply(self, value: Any) -> Union[Optional[bool], Any]:
        return bool(value)

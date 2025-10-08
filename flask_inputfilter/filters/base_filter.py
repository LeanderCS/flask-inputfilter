from __future__ import annotations

import warnings

warnings.warn(
    "Please use `flask_inputfilter.models` for importing BaseFilter "
    "as `flask_inputfilter.filters` is deprecated and will be removed in "
    "future versions.",
    DeprecationWarning,
    stacklevel=2,
)

from flask_inputfilter.models import BaseFilter

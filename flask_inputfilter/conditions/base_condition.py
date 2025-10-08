from __future__ import annotations

import warnings

warnings.warn(
    "Please use `flask_inputfilter.models` for importing BaseCondition "
    "as `flask_inputfilter.conditions` is deprecated and will be removed in "
    "future versions.",
    DeprecationWarning,
    stacklevel=2,
)

from flask_inputfilter.models import BaseCondition

from __future__ import annotations

from typing import Any, List, Optional, Union

from flask_inputfilter.filters import BaseFilter
from flask_inputfilter.models import ExternalApiConfig
from flask_inputfilter.validators import BaseValidator


class FieldModel:
    """FieldModel is a dataclass that represents a field in the input data."""

    def __init__(
        self,
        required: bool = False,
        default: Any = None,
        fallback: Any = None,
        filters: Optional[List[BaseFilter]] = None,
        validators: Optional[List[BaseValidator]] = None,
        steps: Optional[List[Union[BaseFilter, BaseValidator]]] = None,
        external_api: Optional[ExternalApiConfig] = None,
        copy: Optional[str] = None,
    ):
        self.required = required
        self.default = default
        self.fallback = fallback
        self.filters = filters or []
        self.validators = validators or []
        self.steps = steps or []
        self.external_api = external_api
        self.copy = copy

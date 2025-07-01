from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Union

from flask_inputfilter.filters import BaseFilter
from flask_inputfilter.models import ExternalApiConfig
from flask_inputfilter.validators import BaseValidator


@dataclass
class FieldModel:
    """FieldModel is a dataclass that represents a field in the input data."""

    required: bool = False
    default: Any = None
    fallback: Any = None
    filters: list[BaseFilter] = field(default_factory=list)
    validators: list[BaseValidator] = field(default_factory=list)
    steps: list[Union[BaseFilter, BaseValidator]] = field(default_factory=list)
    external_api: Optional[ExternalApiConfig] = None
    copy: Optional[str] = None

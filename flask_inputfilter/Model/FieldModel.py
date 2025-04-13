from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

from flask_inputfilter.Filter import BaseFilter
from flask_inputfilter.Model import ExternalApiConfig
from flask_inputfilter.Validator import BaseValidator


@dataclass
class FieldModel:
    """
    FieldModel is a dataclass that represents a field in the input data.
    """

    required: bool = False
    default: Any = None
    fallback: Any = None
    filters: List[BaseFilter] = field(default_factory=list)
    validators: List[BaseValidator] = field(default_factory=list)
    steps: List[Union[BaseFilter, BaseValidator]] = field(default_factory=list)
    external_api: Optional[ExternalApiConfig] = None
    copy: Optional[str] = None

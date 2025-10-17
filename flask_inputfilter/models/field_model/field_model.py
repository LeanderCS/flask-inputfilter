from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from collections.abc import Callable

    from flask_inputfilter.models import (
        BaseFilter,
        BaseValidator,
        ExternalApiConfig,
    )


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
    computed: Optional[Callable[[dict[str, Any]], Any]] = None
    input_filter: Optional[type] = None

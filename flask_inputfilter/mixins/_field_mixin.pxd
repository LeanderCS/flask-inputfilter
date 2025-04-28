from typing import Any, Dict, List, Union

from flask_inputfilter.conditions import BaseCondition
from flask_inputfilter.filters import BaseFilter
from flask_inputfilter.validators import BaseValidator


cdef class FieldMixin:

    @staticmethod
    cdef object apply_filters(filters: List[BaseFilter], value: Any)
    @staticmethod
    cdef object validate_field(validators: List[BaseValidator], fallback: Any, value: Any)
    @staticmethod
    cdef object apply_steps(steps: List[Union[BaseFilter, BaseValidator]], fallback: Any, value: Any)
    @staticmethod
    cdef void check_conditions(conditions: List[BaseCondition], validated_data: Dict[str, Any]) except *
    @staticmethod
    cdef object check_for_required(field_name: str, required: bool, default: Any, fallback: Any, value: Any)

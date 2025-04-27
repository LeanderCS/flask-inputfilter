from typing import Any, Dict, List, Union

from flask_inputfilter.conditions import BaseCondition
from flask_inputfilter.filters import BaseFilter
from flask_inputfilter.validators import BaseValidator


cdef class FieldMixin:

    @staticmethod
    cdef object applyFilters(filters: List[BaseFilter], value: Any)
    @staticmethod
    cdef object validateField(validators: List[BaseValidator], fallback: Any, value: Any)
    @staticmethod
    cdef object applySteps(steps: List[Union[BaseFilter, BaseValidator]], fallback: Any, value: Any)
    @staticmethod
    cdef void checkConditions(conditions: List[BaseCondition], validated_data: Dict[str, Any]) except *
    @staticmethod
    cdef object checkForRequired(field_name: str,
            required: bool,
            default: Any,
            fallback: Any,
            value: Any,)

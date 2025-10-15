from typing import Any

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, FieldModel, BaseCondition


cdef class ValidationMixin:

    @staticmethod
    cdef object apply_filters(list[BaseFilter] filters1, list[BaseFilter] filters2, object value)

    @staticmethod
    cdef object validate_field(list[BaseValidator] validators1, list[BaseValidator] validators2, object fallback, object value)

    @staticmethod
    cdef object apply_steps(list[BaseFilter | BaseValidator] steps, object fallback, object value)

    @staticmethod
    cdef void check_conditions(list[BaseCondition] conditions, dict[str, Any] validated_data) except *

    @staticmethod
    cdef inline object check_for_required(str field_name, FieldModel field_info, object value)

    @staticmethod
    cdef tuple validate_fields(
        dict[str, FieldModel] fields,
        dict[str, Any] data,
        list[BaseFilter] global_filters,
        list[BaseValidator] global_validators
    )

    @staticmethod
    cdef dict apply_nested_input_filter(
        str field_name,
        object input_filter_class,
        object value
    )

    @staticmethod
    cdef inline object get_field_value(
        str field_name,
        FieldModel field_info,
        dict[str, Any] data,
        dict[str, Any] validated_data
    )

from typing import Any

from flask_inputfilter.models._base_filter cimport BaseFilter
from flask_inputfilter.models._field_model cimport FieldModel


cdef class FieldMixin:

    @staticmethod
    cdef object apply_filters(list[BaseFilter] filters1, list[BaseFilter] filters2, object value)
    @staticmethod
    cdef object validate_field(list validators1, list validators2, object fallback, object value)
    @staticmethod
    cdef object apply_steps(list steps, object fallback, object value)
    @staticmethod
    cdef void check_conditions(list conditions, dict[str, Any] validated_data) except *
    @staticmethod
    cdef object check_for_required(str field_name, FieldModel field_info, object value)
    @staticmethod
    cdef tuple validate_fields(
            dict[str, FieldModel] fields,
            dict[str, Any] data,
            list[BaseFilter] global_filters,
            list global_validators
    )
    @staticmethod
    cdef object get_field_value(str field_name, FieldModel field_info, dict[str, Any] data, dict[str, Any] validated_data)

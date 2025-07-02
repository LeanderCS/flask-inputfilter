from typing import Any

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, FieldModel, BaseCondition, InputFilter


cdef class DataMixin:

    @staticmethod
    cdef bint has_unknown_fields(dict[str, Any] data, dict[str, FieldModel] fields)

    @staticmethod
    cdef dict[str, Any] filter_data(dict[str, Any] data, dict[str, FieldModel] fields, list[BaseFilter] global_filters)

    @staticmethod
    cdef tuple validate_with_conditions(
        dict[str, FieldModel] fields,
        dict[str, Any] data,
        list[BaseFilter] global_filters,
        list[BaseValidator] global_validators,
        list[BaseCondition] conditions
    )

    @staticmethod
    cdef void merge_input_filters(InputFilter target_filter, InputFilter source_filter) except *

    @staticmethod
    cdef void _merge_component_list(list target_list, list source_list) 
# cython: language=c++
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False

from typing import Any

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.mixins.cimports cimport ValidationMixin
from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, FieldModel, BaseCondition, InputFilter

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.algorithm cimport find

DEF LARGE_DATASET_THRESHOLD = 100


cdef class DataMixin:

    @staticmethod
    cdef bint has_unknown_fields(
            dict[str, Any] data,
            dict[str, FieldModel] fields
    ):
        """
        Check if data contains fields not defined in fields configuration.
        Uses optimized lookup strategy based on field count.

        **Parameters:**

        - **data** (*dict[str, Any]*): The input data to check.
        - **fields** (*dict[str, FieldModel]*): The field definitions.

        **Returns:**

        - (*bool*): True if unknown fields exist, False otherwise.
        """
        if not data and fields:
            return True

        for field_name in data.keys():
            if field_name not in fields:
                return True

        return False

    @staticmethod
    cdef dict[str, Any] filter_data(
            dict[str, Any] data,
            dict[str, FieldModel] fields,
            list[BaseFilter] global_filters
    ):
        """
        Filter input data through field-specific and global filters.

        **Parameters:**

        - **data** (*dict[str, Any]*): The input data to filter.
        - **fields** (*dict[str, FieldModel]*): Field definitions with filters.
        - **global_filters** (*list[BaseFilter]*): Global filters to apply.

        **Returns:**

        - (*dict[str, Any]*): The filtered data.
        """
        cdef:
            dict[str, Any] filtered_data = {}
            Py_ssize_t i
            list keys
            list values
            str field_name
            object field_value

        if not data:
            return filtered_data

        keys = list(data.keys())
        values = list(data.values())

        for i in range(len(data)):
            field_name = keys[i]
            field_value = values[i]
            
            if field_name in fields:
                field_value = ValidationMixin.apply_filters(
                    fields[field_name].filters,
                    global_filters,
                    field_value,
                )

            filtered_data[field_name] = field_value

        return filtered_data

    @staticmethod
    cdef tuple validate_with_conditions(
            dict[str, FieldModel] fields,
            dict[str, Any] data,
            list[BaseFilter] global_filters,
            list[BaseValidator] global_validators,
            list[BaseCondition] conditions
    ):
        """
        Complete validation pipeline including conditions check.

        **Parameters:**

        - **fields** (*dict[str, FieldModel]*): Field definitions.
        - **data** (*dict[str, Any]*): Input data to validate.
        - **global_filters** (*list[BaseFilter]*): Global filters.
        - **global_validators** (*list[BaseValidator]*): Global validators.
        - **conditions** (*list[BaseCondition]*): Conditions to check.

        **Returns:**

        - (*tuple*): (validated_data, errors) tuple.
        """
        cdef:
            dict[str, Any] validated_data
            dict[str, str] errors

        validated_data, errors = ValidationMixin.validate_fields(
            fields, data, global_filters, global_validators
        )

        if conditions and not errors:
            try:
                ValidationMixin.check_conditions(conditions, validated_data)
            except ValidationError as e:
                errors["_condition"] = str(e)

        return validated_data, errors

    @staticmethod
    cdef void merge_input_filters(
            InputFilter target_filter,
            InputFilter source_filter
    ) except *:
        """
        Efficiently merge one InputFilter into another.

        **Parameters:**

        - **target_filter** (*InputFilter*): The InputFilter to merge into.
        - **source_filter** (*InputFilter*): The InputFilter to merge from.
        """
        cdef:
            Py_ssize_t i, n
            dict source_inputs = source_filter.get_inputs()
            list keys = list(source_inputs.keys()) if source_inputs else []
            list new_fields = list(source_inputs.values()) if source_inputs else []
            str method
            bytes encoded_method

        n = len(keys)
        for i in range(n):
            target_filter.fields[keys[i]] = new_fields[i]

        target_filter.conditions.extend(source_filter.conditions)

        DataMixin._merge_component_list(
            target_filter.global_filters,
            source_filter.global_filters
        )

        DataMixin._merge_component_list(
            target_filter.global_validators,
            source_filter.global_validators
        )

    @staticmethod
    cdef void _merge_component_list(list target_list, list source_list):
        """
        Helper method to merge component lists avoiding duplicates by type.

        **Parameters:**

        - **target_list** (*list*): The list to merge into.
        - **source_list** (*list*): The list to merge from.
        """
        cdef dict existing_type_map
        
        for component in source_list:
            existing_type_map = {
                type(v): i for i, v in enumerate(target_list)
            }
            if type(component) in existing_type_map:
                target_list[existing_type_map[type(component)]] = component
            else:
                target_list.append(component) 
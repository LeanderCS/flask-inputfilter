# cython: language=c++
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

from typing import Any

from flask_inputfilter.exceptions import ValidationError

from flask_inputfilter.mixins.cimports cimport ValidationMixin

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, FieldModel, BaseCondition, InputFilter

# Compile-time constants for performance thresholds
DEF LARGE_DATASET_THRESHOLD = 10
DEF SMALL_DICT_THRESHOLD = 5


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

        cdef:
            set field_set
            Py_ssize_t field_count = len(fields)
            Py_ssize_t data_count = len(data)

        if field_count > LARGE_DATASET_THRESHOLD and data_count > SMALL_DICT_THRESHOLD:
            field_set = set(fields.keys())
            for field_name in data.keys():
                if field_name not in field_set:
                    return True
        elif data_count < field_count:
            for field_name in data.keys():
                if field_name not in fields:
                    return True
        else:
            return bool(set(data.keys()) - set(fields.keys()))

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
            Py_ssize_t i, n = len(data) if data is not None else 0
            list keys
            list values
            str field_name
            object field_value
            FieldModel field_info

        if n == 0:
            return filtered_data

        keys = list(data.keys())
        values = list(data.values())

        for i in range(n):
            field_name = keys[i]
            field_value = values[i]

            field_info = fields.get(field_name)
            if field_info is not None:
                field_value = ValidationMixin.apply_filters(
                    field_info.filters,
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

        # Validate fields
        validated_data, errors = ValidationMixin.validate_fields(
            fields, data, global_filters, global_validators
        )

        # Check conditions only if present and no errors yet
        if conditions is not None and len(conditions) > 0 and not errors:
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
            list keys
            list new_fields
        
        if source_inputs:
            keys = list(source_inputs.keys())
            new_fields = list(source_inputs.values())
            n = len(keys)

            for i in range(n):
                target_filter.fields[keys[i]] = new_fields[i]
        else:
            n = 0
        
        # Merge conditions
        target_filter.conditions.extend(source_filter.conditions)

        # Merge global filters (avoid duplicates by type)
        DataMixin._merge_component_list(
            target_filter.global_filters, 
            source_filter.global_filters
        )

        # Merge global validators (avoid duplicates by type)
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
        cdef:
            dict existing_type_map = {}
            Py_ssize_t i, n = len(target_list)
            object component
            type component_type

        for i in range(n):
            existing_type_map[type(target_list[i])] = i

        for component in source_list:
            component_type = type(component)
            if component_type in existing_type_map:
                target_list[existing_type_map[component_type]] = component
            else:
                target_list.append(component)
                existing_type_map[component_type] = len(target_list) - 1

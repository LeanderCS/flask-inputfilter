from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flask_inputfilter.exceptions import ValidationError

if TYPE_CHECKING:
    from flask_inputfilter import InputFilter
    from flask_inputfilter.models import (
        BaseCondition,
        BaseFilter,
        BaseValidator,
        FieldModel,
    )

LARGE_DATASET_THRESHOLD = 10


class DataMixin:
    __slots__ = ()

    @staticmethod
    def has_unknown_fields(
        data: dict[str, Any],
        fields: dict[str, FieldModel],
    ) -> bool:
        """
        Check if data contains fields not defined in fields configuration. Uses
        optimized lookup strategy based on field count.

        **Parameters:**

        - **data** (*dict[str, Any]*): The input data to check.
        - **fields** (*dict[str, FieldModel]*): The field definitions.

        **Returns:**

        - (*bool*): True if unknown fields exist, False otherwise.
        """
        if not data and fields:
            return True

        return any(field_name not in fields for field_name in data)

    @staticmethod
    def filter_data(
        data: dict[str, Any],
        fields: dict[str, FieldModel],
        global_filters: list[BaseFilter],
    ) -> dict[str, Any]:
        """
        Filter input data through field-specific and global filters.

        **Parameters:**

        - **data** (*dict[str, Any]*): The input data to filter.
        - **fields** (*dict[str, FieldModel]*): Field definitions with filters.
        - **global_filters** (*list[BaseFilter]*): Global filters to apply.

        **Returns:**

        - (*dict[str, Any]*): The filtered data.
        """
        # Import here to avoid circular imports
        from flask_inputfilter.mixins import ValidationMixin

        filtered_data = {}
        for field_name, field_value in data.items():
            if field_name in fields:
                field_value = ValidationMixin.apply_filters(
                    fields[field_name].filters,
                    global_filters,
                    field_value,
                )
            filtered_data[field_name] = field_value
        return filtered_data

    @staticmethod
    def validate_with_conditions(
        fields: dict[str, FieldModel],
        data: dict[str, Any],
        global_filters: list[BaseFilter],
        global_validators: list[BaseValidator],
        conditions: list[BaseCondition],
    ) -> tuple[dict[str, Any], dict[str, str]]:
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
        from flask_inputfilter.mixins import ValidationMixin

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
    def merge_input_filters(
        target_filter: InputFilter,
        source_filter: InputFilter,
    ) -> None:
        """
        Efficiently merge one InputFilter into another.

        **Parameters:**

        - **target_filter** (*InputFilter*): The InputFilter to merge into.
        - **source_filter** (*InputFilter*): The InputFilter to merge from.
        """
        # Merge fields
        target_filter.fields.update(source_filter.get_inputs())

        # Merge conditions
        target_filter.conditions.extend(source_filter.conditions)

        # Merge global filters (avoid duplicates by type)
        DataMixin._merge_component_list(
            target_filter.global_filters,
            source_filter.global_filters,
        )

        # Merge global validators (avoid duplicates by type)
        DataMixin._merge_component_list(
            target_filter.global_validators,
            source_filter.global_validators,
        )

    @staticmethod
    def _merge_component_list(
        target_list: list,
        source_list: list,
    ) -> None:
        """
        Helper method to merge component lists avoiding duplicates by type.

        **Parameters:**

        - **target_list** (*list*): The list to merge into.
        - **source_list** (*list*): The list to merge from.
        """
        existing_type_map = {type(v): i for i, v in enumerate(target_list)}

        for component in source_list:
            component_type = type(component)
            if component_type in existing_type_map:
                target_list[existing_type_map[component_type]] = component
            else:
                target_list.append(component)

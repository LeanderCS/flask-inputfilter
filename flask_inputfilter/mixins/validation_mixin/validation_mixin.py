from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING, Any, Union

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseFilter, BaseValidator, FieldModel

if TYPE_CHECKING:
    from flask_inputfilter.models import BaseCondition


class ValidationMixin:
    __slots__ = ()

    @staticmethod
    def apply_filters(
        filters1: list[BaseFilter],
        filters2: list[BaseFilter],
        value: Any,
    ) -> Any:
        """
        Apply filters to the field value.

        **Parameters:**

        - **filters1** (*list[BaseFilter]*): A list of filters to apply to the
          value.
        - **filters2** (*list[BaseFilter]*): A list of filters to apply to the
          value.
        - **value** (*Any*): The value to be processed by the filters.

        **Returns:**

        - (*Any*): The processed value after applying all filters.
          If the value is None, None is returned.
        """
        if value is None:
            return None

        for filter in chain(filters1, filters2):
            value = filter.apply(value)

        return value

    @staticmethod
    def validate_field(
        validators1: list[BaseValidator],
        validators2: list[BaseValidator],
        fallback: Any,
        value: Any,
    ) -> Any:
        """
        Validate the field value.

        **Parameters:**

        - **validators1** (*list[BaseValidator]*): A list of validators to
          apply to the field value.
        - **validators2** (*list[BaseValidator]*): A list of validators to
          apply to the field value.
        - **fallback** (*Any*): A fallback value to return if validation
          fails.
        - **value** (*Any*): The value to be validated.

        **Returns:**

        - (*Any*): The validated value if all validators pass. If validation
          fails and a fallback is provided, the fallback value is returned.
        """
        if value is None:
            return None

        try:
            for validator in chain(validators1, validators2):
                validator.validate(value)
        except ValidationError:
            if fallback is None:
                raise

            return fallback

        return value

    @staticmethod
    def apply_steps(
        steps: list[Union[BaseFilter, BaseValidator]],
        fallback: Any,
        value: Any,
    ) -> Any:
        """
        Apply multiple filters and validators in a specific order.

        This method processes a given value by sequentially applying a list of
        filters and validators. Filters modify the value, while validators
        ensure the value meets specific criteria. If a validation error occurs
        and a fallback value is provided, the fallback is returned. Otherwise,
        the validation error is raised.

        **Parameters:**

        - **steps** (*list[Union[BaseFilter, BaseValidator]]*):
          A list of filters and validators to be applied in order.
        - **fallback** (*Any*):
          A fallback value to return if validation fails.
        - **value** (*Any*):
          The initial value to be processed.

        **Returns:**

        - (*Any*): The processed value after applying all filters and
          validators. If a validation error occurs and a fallback is
          provided, the fallback value is returned.

        **Raises:**

        - **ValidationError:** If validation fails and no fallback value is
          provided.
        """
        if value is None:
            return None

        try:
            for step in steps:
                if isinstance(step, BaseFilter):
                    value = step.apply(value)
                elif isinstance(step, BaseValidator):
                    step.validate(value)
        except ValidationError:
            if fallback is None:
                raise
            return fallback
        return value

    @staticmethod
    def check_conditions(
        conditions: list[BaseCondition],
        validated_data: dict[str, Any],
    ) -> None:
        """
        Checks if all conditions are met.

        This method iterates through all registered conditions and checks
        if they are satisfied based on the provided validated data. If any
        condition is not met, a ValidationError is raised with an appropriate
        message indicating which condition failed.

        **Parameters:**

        - **conditions** (*list[BaseCondition]*):
          A list of conditions to be checked against the validated data.
        - **validated_data** (*dict[str, Any]*):
          The validated data to check against the conditions.
        """
        for condition in conditions:
            if not condition.check(validated_data):
                raise ValidationError(
                    f"Condition '{condition.__class__.__name__}' not met."
                )

    @staticmethod
    def check_for_required(
        field_name: str,
        field_info: FieldModel,
        value: Any,
    ) -> Any:
        """
        Determine the value of the field, considering the required and fallback
        attributes.

        If the field is not required and no value is provided, the default
        value is returned. If the field is required and no value is provided,
        the fallback value is returned. If no of the above conditions are met,
        a ValidationError is raised.

        **Parameters:**

        - **field_name** (*str*): The name of the field being processed.
        - **field_info** (*FieldModel*): The object of the field.
        - **value** (*Any*): The current value of the field being processed.

        **Returns:**

        - (*Any*): The determined value of the field after considering
          required, default, and fallback attributes.

        **Raises:**

        - **ValidationError**:
          If the field is required and no value or fallback is provided.
        """
        if value is not None:
            return value

        if not field_info.required:
            return field_info.default

        if field_info.fallback is not None:
            return field_info.fallback

        raise ValidationError(f"Field '{field_name}' is required.")

    @staticmethod
    def validate_fields(
        fields: dict[str, Any],
        data: dict[str, Any],
        global_filters: list[BaseFilter],
        global_validators: list[BaseValidator],
    ) -> tuple:
        """Process and validate all fields."""

        validated_data = {}
        errors = {}

        for field_name, field_info in fields.items():
            try:
                value = ValidationMixin.get_field_value(
                    field_name, field_info, data, validated_data
                )

                value = ValidationMixin.apply_filters(
                    field_info.filters, global_filters, value
                )

                value = ValidationMixin.validate_field(
                    field_info.validators,
                    global_validators,
                    field_info.fallback,
                    value,
                )

                value = ValidationMixin.apply_steps(
                    field_info.steps, field_info.fallback, value
                )

                value = ValidationMixin.check_for_required(
                    field_name, field_info, value
                )

                if field_info.input_filter is not None and value is not None:
                    value = ValidationMixin.apply_nested_input_filter(
                        field_name, field_info.input_filter, value
                    )

                validated_data[field_name] = value
            except ValidationError as e:
                errors[field_name] = str(e)

        return validated_data, errors

    @staticmethod
    def apply_nested_input_filter(
        field_name: str,
        input_filter_class: type,
        value: Any,
    ) -> dict[str, Any]:
        """
        Apply nested InputFilter validation to a field value.

        **Parameters:**

        - **field_name** (*str*): The name of the field being validated.
        - **input_filter_class** (*type*): The InputFilter class to
          use for validation.
        - **value** (*Any*): The value to validate (must be a dict).

        **Returns:**

        - (*dict[str, Any]*): The validated nested data as a dictionary.

        **Raises:**

        - **ValidationError**: If the value is not a dict or if nested
          validation fails.
        """
        if not isinstance(value, dict):
            raise ValidationError(
                f"Field '{field_name}' must be a dict for nested InputFilter "
                f"validation, got {type(value).__name__}."
            )

        try:
            return input_filter_class().validate_data(value)
        except ValidationError as e:
            raise ValidationError(
                f"Nested validation failed for field '{field_name}': {e!s}"
            ) from e

    @staticmethod
    def get_field_value(
        field_name: str,
        field_info: FieldModel,
        data: dict[str, Any],
        validated_data: dict[str, Any],
    ) -> Any:
        """
        Retrieve the value of a field based on its configuration.

        **Parameters:**

        - **field_name** (*str*): The name of the field to retrieve.
        - **field_info** (*FieldModel*): The object containing field
          configuration, including copy, external_api, and fallback
          attributes.
        - **data** (*dict[str, Any]*): The original data dictionary from which
          the field value is to be retrieved.
        - **validated_data** (*dict[str, Any]*): The dictionary containing
          already validated data, which may include copied or externally
          fetched values.

        **Returns:**

        - (*Any*): The value of the field, either from the validated data,
          copied from another field, fetched from an external API, or directly
          from the original data dictionary.
        """
        if field_info.computed:
            try:
                return field_info.computed(validated_data)
            except Exception:  # noqa: BLE001
                return None
        if field_info.copy:
            return validated_data.get(field_info.copy)
        if field_info.external_api:
            # Import here to avoid circular imports
            from flask_inputfilter.mixins import ExternalApiMixin

            return ExternalApiMixin.call_external_api(
                field_info.external_api, field_info.fallback, validated_data
            )
        return data.get(field_name)

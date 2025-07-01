# cython: language=c++

import cython

from flask_inputfilter.exceptions import ValidationError

from flask_inputfilter.mixins._external_api_mixin cimport ExternalApiMixin
from flask_inputfilter.models._base_filter cimport BaseFilter
from flask_inputfilter.models._field_model cimport FieldModel

from flask_inputfilter.validators import BaseValidator


cdef class FieldMixin:

    @staticmethod
    @cython.exceptval(check=False)
    cdef object apply_filters(list[BaseFilter] filters1, list[BaseFilter] filters2, object value):
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

        cdef:
            int i, n
            object current_filter

        if filters1:
            n = len(filters1)
            for i in range(n):
                current_filter = filters1[i]
                value = current_filter.apply(value)

        if filters2:
            n = len(filters2)
            for i in range(n):
                current_filter = filters2[i]
                value = current_filter.apply(value)

        return value

    @staticmethod
    cdef object apply_steps(
            list steps,
            object fallback,
            object value
    ):
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

        cdef:
            int i, n = len(steps)
            object current_step

        try:
            for i in range(n):
                current_step = steps[i]
                if isinstance(current_step, BaseFilter):
                    value = current_step.apply(value)
                elif isinstance(current_step, BaseValidator):
                    current_step.validate(value)
        except ValidationError:
            if fallback is None:
                raise
            return fallback
        return value

    @staticmethod
    cdef void check_conditions(list conditions, dict[str, Any] validated_data) except *:
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
        cdef:
            int i, n = len(conditions)
            object current_condition

        for i in range(n):
            current_condition = conditions[i]
            if not current_condition.check(validated_data):
                raise ValidationError(
                    f"Condition '{current_condition.__class__.__name__}' "
                    f"not met."
                )

    @staticmethod
    cdef inline object check_for_required(
            str field_name,
            FieldModel field_info,
            object value,
    ):
        """
        Determine the value of the field, considering the required and
        fallback attributes.

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
    cdef object validate_field(
            list validators1,
            list validators2,
            object fallback,
            object value
    ):
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

        cdef:
            int i, n
            object current_validator

        try:
            if validators1:
                n = len(validators1)
                for i in range(n):
                    current_validator = validators1[i]
                    current_validator.validate(value)

            if validators2:
                n = len(validators2)
                for i in range(n):
                    current_validator = validators2[i]
                    current_validator.validate(value)
        except ValidationError:
            if fallback is None:
                raise

            return fallback

        return value

    @staticmethod
    cdef tuple validate_fields(
            dict[str, FieldModel] fields,
            dict[str, Any] data,
            list[BaseFilter] global_filters,
            list global_validators
    ):
        """
        Validate multiple fields based on their configurations.

        **Parameters:**

        - **fields** (*dict[str, FieldModel]*): A dictionary where keys are 
          field names and values are FieldModel objects containing field 
          configurations.
        - **data** (*dict[str, Any]*): The input data dictionary containing
          the values to be validated.
        - **global_filters** (*list[BaseFilter]*): A list of global filters
          to be applied to all fields.
        - **global_validators** (*list[BaseValidator]*): A list of global
          validators to be applied to all fields.

        **Returns:**

        - (*tuple*): A tuple containing two dictionaries:
            - **validated_data** (*dict[str, Any]*): A dictionary of field names
              and their validated values.
            - **errors** (*dict[str, str]*): A dictionary of field names and
              error messages for any validation failures.
        """
        cdef:
            dict validated_data = {}, errors = {}
            int i, n = len(fields)
            list field_names = list(fields.keys()), field_infos = list(fields.values())
            object value

        for i in range(n):
            field_name = field_names[i]
            field_info = field_infos[i]

            try:
                # Get initial value
                value = FieldMixin.get_field_value(
                    field_name,
                    field_info,
                    data,
                    validated_data
                )

                # Apply filters
                value = FieldMixin.apply_filters(
                    field_info.filters,
                    global_filters,
                    value
                )

                # Apply validators
                value = FieldMixin.validate_field(
                    field_info.validators,
                    global_validators,
                    field_info.fallback,
                    value
                )

                # Apply steps
                value = FieldMixin.apply_steps(
                    field_info.steps,
                    field_info.fallback,
                    value
                )

                # Handle required fields and defaults
                value = FieldMixin.check_for_required(
                    field_name,
                    field_info,
                    value
                )

                validated_data[field_name] = value
            except ValidationError as e:
                errors[field_name] = str(e)

        return validated_data, errors

    @staticmethod
    cdef inline object get_field_value(
            str field_name,
            FieldModel field_info,
            dict[str, Any] data,
            dict[str, Any] validated_data
    ):
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
        if field_info.copy:
            return validated_data.get(field_info.copy)
        elif field_info.external_api:
            return ExternalApiMixin.call_external_api(
                field_info.external_api,
                field_info.fallback,
                validated_data
            )
        else:
            return data.get(field_name)

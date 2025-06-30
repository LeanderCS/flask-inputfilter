# cython: language=c++
from typing import Union

import cython

from flask_inputfilter.conditions import BaseCondition
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import BaseFilter
from flask_inputfilter.validators import BaseValidator


cdef class FieldMixin:
    @staticmethod
    @cython.exceptval(check=False)
    cdef object apply_filters(list filters, object value):
        """
        Apply filters to the field value.

        Args:
            filters (list[BaseFilter]): A list of filters to apply to the 
                value.
            value (Any): The value to be processed by the filters.

        Returns:
            Any: The processed value after applying all filters. 
                If the value is None, None is returned.
        """
        if value is None:
            return None

        cdef:
            int i
            int n = len(filters)
            object current_filter

        for i in range(n):
            current_filter = filters[i]
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

        Args:
            steps (list[Union[BaseFilter, BaseValidator]]): 
                A list of filters and validators to be applied in order.
            fallback (Any): 
                A fallback value to return if validation fails.
            value (Any): 
                The initial value to be processed.

        Returns:
            Any: The processed value after applying all filters and validators. 
                If a validation error occurs and a fallback is provided, the 
                fallback value is returned.

        Raises:
            ValidationError: If validation fails and no fallback value is 
                provided.
        """
        if value is None:
            return None

        cdef:
            int i
            int n = len(steps)
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
    cdef void check_conditions(list conditions, dict validated_data) except *:
        """
        Checks if all conditions are met.

        This method iterates through all registered conditions and checks
        if they are satisfied based on the provided validated data. If any
        condition is not met, a ValidationError is raised with an appropriate
        message indicating which condition failed.

        Args:
            conditions (list[BaseCondition]):
                A list of conditions to be checked against the validated data.
            validated_data (dict[str, Any]):
                The validated data to check against the conditions.
        """
        cdef:
            int i
            int n = len(conditions)
            object current_condition

        for i in range(n):
            current_condition = conditions[i]
            if not current_condition.check(validated_data):
                raise ValidationError(
                    f"Condition '{current_condition.__class__.__name__}' not met."
                )

    @staticmethod
    cdef inline object check_for_required(
            str field_name,
            bint required,
            object default,
            object fallback,
            object value,
    ):
        """
        Determine the value of the field, considering the required and
        fallback attributes.

        If the field is not required and no value is provided, the default
        value is returned. If the field is required and no value is provided,
        the fallback value is returned. If no of the above conditions are met,
        a ValidationError is raised.

        Args:
            field_name (str): The name of the field being processed.
            required (bool): Indicates whether the field is required.
            default (Any): The default value to use if the field is not provided and not required.
            fallback (Any): The fallback value to use if the field is required but not provided.
            value (Any): The current value of the field being processed.

        Returns:
            Any: The determined value of the field after considering required, default, and fallback attributes.

        Raises:
            ValidationError: If the field is required and no value or fallback is provided.
        """
        if value is not None:
            return value

        if not required:
            return default

        if fallback is not None:
            return fallback

        raise ValidationError(f"Field '{field_name}' is required.")

    @staticmethod
    cdef object validate_field(
            list validators, object fallback, object value
    ):
        """
        Validate the field value.

        Args:
            validators (list[BaseValidator]): A list of validators to apply 
                to the field value.
            fallback (Any): A fallback value to return if validation fails.
            value (Any): The value to be validated.

        Returns:
            Any: The validated value if all validators pass. If validation 
                fails and a fallback is provided, the fallback value is 
                returned.
        """
        if value is None:
            return None

        cdef:
            int i
            int n = len(validators)
            object current_validator

        try:
            for i in range(n):
                current_validator = validators[i]
                current_validator.validate(value)
        except ValidationError:
            if fallback is None:
                raise

            return fallback

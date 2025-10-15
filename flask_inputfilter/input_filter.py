from __future__ import annotations

import dataclasses
import inspect
import json
import logging
import sys
import warnings
from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar, Union

from flask import Response, g, request

from flask_inputfilter.declarative import FieldDescriptor
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.mixins import DataMixin
from flask_inputfilter.models import BaseFilter, ExternalApiConfig, FieldModel

if TYPE_CHECKING:
    from collections.abc import Callable

    from flask_inputfilter.models import BaseCondition, BaseValidator

T = TypeVar("T")

_INTERNED_STRINGS = {
    "_condition": sys.intern("_condition"),
    "_error": sys.intern("_error"),
    "copy": sys.intern("copy"),
    "default": sys.intern("default"),
    "DELETE": sys.intern("DELETE"),
    "external_api": sys.intern("external_api"),
    "fallback": sys.intern("fallback"),
    "filters": sys.intern("filters"),
    "GET": sys.intern("GET"),
    "PATCH": sys.intern("PATCH"),
    "POST": sys.intern("POST"),
    "PUT": sys.intern("PUT"),
    "required": sys.intern("required"),
    "steps": sys.intern("steps"),
    "validators": sys.intern("validators"),
}


class InputFilter:
    """Base class for all input filters."""

    def __init__(self, methods: Optional[list[str]] = None) -> None:
        self.methods: list[str] = methods or [
            "DELETE",
            "GET",
            "PATCH",
            "POST",
            "PUT",
        ]
        self.fields: dict[str, FieldModel] = {}
        self.conditions: list[BaseCondition] = []
        self.global_filters: list[BaseFilter] = []
        self.global_validators: list[BaseValidator] = []
        self.data: dict[str, Any] = {}
        self.validated_data: dict[str, Any] = {}
        self.errors: dict[str, str] = {}
        self.model_class: Optional[Type[T]] = None

        self._register_decorator_components()

    def is_valid(self) -> bool:
        """
        Checks if the object's state or its attributes meet certain conditions
        to be considered valid. This function is typically used to ensure that
        the current state complies with specific requirements or rules.

        Returns:
            bool: Returns True if the state or attributes of the object fulfill
                all required conditions; otherwise, returns False.
        """
        try:
            self.validate_data()

        except ValidationError as e:
            self.errors = e.args[0]
            return False

        return True

    @classmethod
    def validate(
        cls,
    ) -> Callable:
        """
        Decorator for validating input data in routes.

        Args:
            cls

        Returns:
            Callable
        """

        def decorator(
            f: Callable,
        ) -> Callable:
            """
            Decorator function to validate input data for a Flask route.

            Args:
                f (Callable): The Flask route function to be decorated.

            Returns:
                Callable: The wrapped function with input validation.
            """

            def wrapper(
                *args: Any, **kwargs: Any
            ) -> Union[Response, tuple[Any, dict[str, Any]]]:
                """
                Wrapper function to handle input validation and error handling
                for the decorated route function.

                Args:
                    *args: Positional arguments for the route function.
                    **kwargs: Keyword arguments for the route function.

                Returns:
                    Union[Response, tuple[Any, dict[str, Any]]]: The response
                        from the route function or an error response.
                """
                input_filter = cls()
                if request.method not in input_filter.methods:
                    return Response(status=405)

                if request.is_json:
                    data = request.get_json(cache=True)
                    if not isinstance(data, dict):
                        data = {}
                else:
                    data = dict(request.args)

                try:
                    if kwargs:
                        data.update(kwargs)

                    input_filter.data = data
                    input_filter.validated_data = {}
                    input_filter.errors = {}

                    g.validated_data = input_filter.validate_data()

                except ValidationError as e:
                    return Response(
                        status=400,
                        response=json.dumps(e.args[0]),
                        mimetype="application/json",
                    )

                except Exception:
                    logging.exception(
                        "An unexpected exception occurred while "
                        "validating input data.",
                    )
                    return Response(status=500)

                return f(*args, **kwargs)

            return wrapper

        return decorator

    def validate_data(
        self, data: Optional[dict[str, Any]] = None
    ) -> Union[dict[str, Any], Type[T]]:
        """
        Validates input data against defined field rules, including applying
        filters, validators, custom logic steps, and fallback mechanisms. The
        validation process also ensures the required fields are handled
        appropriately and conditions are checked after processing.

        Args:
            data (dict[str, Any]): A dictionary containing the input data to
                be validated where keys represent field names and values
                represent the corresponding data.

        Returns:
            Union[dict[str, Any], Type[T]]: A dictionary containing the
                validated data with any modifications, default values,
                or processed values as per the defined validation rules.

        Raises:
            Any errors raised during external API calls, validation, or
                logical steps execution of the respective fields or conditions
                will propagate without explicit handling here.
        """
        data = data or self.data

        validated_data, errors = DataMixin.validate_with_conditions(
            self.fields,
            data,
            self.global_filters,
            self.global_validators,
            self.conditions,
        )

        if errors:
            raise ValidationError(errors)

        self.validated_data = validated_data
        return self._serialize()

    def add_condition(self, condition: BaseCondition) -> None:
        """
        Add a condition to the input filter.

        Args:
            condition (BaseCondition): The condition to add.
        """
        warnings.warn(
            "Using 'add_condition' is deprecated, use 'condition()' "
            "instead. https://leandercs.github.io/flask-inputfilter"
            "/options/declarative_api.html",
            DeprecationWarning,
            stacklevel=2,
        )
        self.conditions.append(condition)

    def _register_decorator_components(self) -> None:
        """Register decorator-based components from the current class and
        inheritance chain."""
        cls = self.__class__

        added_conditions = set()
        added_global_validators = set()
        added_global_filters = set()

        for base_cls in reversed(cls.__mro__):
            if base_cls is object:
                continue

            for attr_name, attr_value in base_cls.__dict__.items():
                if attr_name.startswith("_"):
                    continue

                if isinstance(attr_value, FieldDescriptor):
                    self.fields[attr_name] = FieldModel(
                        attr_value.required,
                        attr_value.default,
                        attr_value.fallback,
                        attr_value.filters,
                        attr_value.validators,
                        attr_value.steps,
                        attr_value.external_api,
                        attr_value.copy,
                        attr_value.computed,
                        attr_value.input_filter,
                    )

            conditions = getattr(base_cls, "_conditions", None)
            if conditions is not None:
                for condition in conditions:
                    condition_id = id(condition)
                    if condition_id not in added_conditions:
                        self.conditions.append(condition)
                        added_conditions.add(condition_id)

            validators = getattr(base_cls, "_global_validators", None)
            if validators is not None:
                for validator in validators:
                    validator_id = id(validator)
                    if validator_id not in added_global_validators:
                        self.global_validators.append(validator)
                        added_global_validators.add(validator_id)

            filters = getattr(base_cls, "_global_filters", None)
            if filters is not None:
                for filter_instance in filters:
                    filter_id = id(filter_instance)
                    if filter_id not in added_global_filters:
                        self.global_filters.append(filter_instance)
                        added_global_filters.add(filter_id)

        if hasattr(cls, "_model"):
            self.model_class = cls._model

    def get_conditions(self) -> list[BaseCondition]:
        """
        Retrieve the list of all registered conditions.

        This function provides access to the conditions that have been
        registered and stored. Each condition in the returned list
        is represented as an instance of the BaseCondition type.

        Returns:
            list[BaseCondition]: A list containing all currently registered
                instances of BaseCondition.
        """
        return self.conditions

    def set_data(self, data: dict[str, Any]) -> None:
        """
        Filters and sets the provided data into the object's internal storage,
        ensuring that only the specified fields are considered and their values
        are processed through defined filters.

        Parameters:
            data (dict[str, Any]):
                The input dictionary containing key-value pairs where keys
                represent field names and values represent the associated
                data to be filtered and stored.
        """
        self.data = DataMixin.filter_data(
            data,
            self.fields,
            self.global_filters,
        )

    def get_value(self, name: str) -> Any:
        """
        This method retrieves a value associated with the provided name. It
        searches for the value based on the given identifier and returns the
        corresponding result. If no value is found, it typically returns a
        default or fallback output. The method aims to provide flexibility in
        retrieving data without explicitly specifying the details of the
        underlying implementation.

        Args:
            name (str): A string that represents the identifier for which the
                 corresponding value is being retrieved. It is used to perform
                 the lookup.

        Returns:
            Any: The retrieved value associated with the given name. The
                 specific type of this value is dependent on the
                 implementation and the data being accessed.
        """
        return self.validated_data.get(name)

    def get_values(self) -> dict[str, Any]:
        """
        Retrieves a dictionary of key-value pairs from the current object. This
        method provides access to the internal state or configuration of the
        object in a dictionary format, where keys are strings and values can be
        of various types depending on the object's design.

        Returns:
            dict[str, Any]: A dictionary containing string keys and their
                            corresponding values of any data type.
        """
        return self.validated_data

    def get_raw_value(self, name: str) -> Any:
        """
        Fetches the raw value associated with the provided key.

        This method is used to retrieve the underlying value linked to the
        given key without applying any transformations or validations. It
        directly fetches the raw stored value and is typically used in
        scenarios where the raw data is needed for processing or debugging
        purposes.

        Args:
            name (str): The name of the key whose raw value is to be
                retrieved.

        Returns:
            Any: The raw value associated with the provided key.
        """
        return self.data.get(name)

    def get_raw_values(self) -> dict[str, Any]:
        """
        Retrieves raw values from a given source and returns them as a
        dictionary.

        This method is used to fetch and return unprocessed or raw data in
        the form of a dictionary where the keys are strings, representing
        the identifiers, and the values are of any data type.

        Returns:
            dict[str, Any]: A dictionary containing the raw values retrieved.
               The keys are strings representing the identifiers, and the
               values can be of any type, depending on the source
               being accessed.
        """
        if not self.fields:
            return {}

        # Use optimized intersection for larger datasets
        if len(self.fields) > 10:
            field_set = set(self.fields.keys())
            data_set = set(self.data.keys())
            common_fields = field_set & data_set
            return {field: self.data[field] for field in common_fields}
        return {
            field: self.data[field]
            for field in self.fields
            if field in self.data
        }

    def get_unfiltered_data(self) -> dict[str, Any]:
        """
        Fetches unfiltered data from the data source.

        This method retrieves data without any filtering, processing, or
        manipulations applied. It is intended to provide raw data that has
        not been altered since being retrieved from its source. The usage
        of this method should be limited to scenarios where unprocessed data
        is required, as it does not perform any validations or checks.

        Returns:
            dict[str, Any]: The unfiltered, raw data retrieved from the
                 data source. The return type may vary based on the
                 specific implementation of the data source.
        """
        return self.data

    def set_unfiltered_data(self, data: dict[str, Any]) -> None:
        """
        Sets unfiltered data for the current instance. This method assigns a
        given dictionary of data to the instance for further processing. It
        updates the internal state using the provided data.

        Parameters:
            data (dict[str, Any]): A dictionary containing the unfiltered
                data to be associated with the instance.
        """
        self.data = data

    def has_unknown(self) -> bool:
        """
        Checks whether any values in the current data do not have corresponding
        configurations in the defined fields.

        Returns:
            bool: True if there are any unknown fields; False otherwise.
        """
        return DataMixin.has_unknown_fields(self.data, self.fields)

    def get_error_message(self, field_name: str) -> Optional[str]:
        """
        Retrieves and returns a predefined error message.

        This method is intended to provide a consistent error message
        to be used across the application when an error occurs. The
        message is predefined and does not accept any parameters.
        The exact content of the error message may vary based on
        specific implementation, but it is designed to convey meaningful
        information about the nature of an error.

        Args:
            field_name (str): The name of the field for which the error
                message is being retrieved.

        Returns:
            Optional[str]: A string representing the predefined error message.
        """
        return self.errors.get(field_name)

    def get_error_messages(self) -> dict[str, str]:
        """
        Retrieves all error messages associated with the fields in the input
        filter.

        This method aggregates and returns a dictionary of error messages
        where the keys represent field names, and the values are their
        respective error messages.

        Returns:
            dict[str, str]: A dictionary containing field names as keys and
                            their corresponding error messages as values.
        """
        return self.errors

    def add(
        self,
        name: str,
        required: bool = False,
        default: Any = None,
        fallback: Any = None,
        filters: Optional[list[BaseFilter]] = None,
        validators: Optional[list[BaseValidator]] = None,
        steps: Optional[list[Union[BaseFilter, BaseValidator]]] = None,
        external_api: Optional[ExternalApiConfig] = None,
        copy: Optional[str] = None,
    ) -> None:
        """
        Add the field to the input filter.

        Args:
            name (str): The name of the field.

            required (Optional[bool]): Whether the field is required.

            default (Optional[Any]): The default value of the field.

            fallback (Optional[Any]): The fallback value of the field, if
                validations fails or field None, although it is required.

            filters (Optional[list[BaseFilter]]): The filters to apply to
                the field value.

            validators (Optional[list[BaseValidator]]): The validators to
                apply to the field value.

            steps (Optional[list[Union[BaseFilter, BaseValidator]]]): Allows
                to apply multiple filters and validators in a specific order.

            external_api (Optional[ExternalApiConfig]): Configuration for an
                external API call.

            copy (Optional[str]): The name of the field to copy the value
                from.
        """
        warnings.warn(
            "Using 'add' is deprecated, use 'field()' "
            "instead. https://leandercs.github.io/flask-inputfilter"
            "/options/declarative_api.html",
            DeprecationWarning,
            stacklevel=2,
        )
        if name in self.fields:
            raise ValueError(f"Field '{name}' already exists.")

        self.fields[name] = FieldModel(
            required,
            default,
            fallback,
            filters or [],
            validators or [],
            steps or [],
            external_api,
            copy,
        )

    def has(self, field_name: str) -> bool:
        """
        This method checks the existence of a specific field within the input
        filter values, identified by its field name. It does not return a
        value, serving purely as a validation or existence check mechanism.

        Args:
            field_name (str): The name of the field to check for existence.

        Returns:
            bool: True if the field exists in the input filter,
                otherwise False.
        """
        return field_name in self.fields

    def get_input(self, field_name: str) -> Optional[FieldModel]:
        """
        Represents a method to retrieve a field by its name.

        This method allows fetching the configuration of a specific field
        within the object, using its name as a string. It ensures
        compatibility with various field names and provides a generic
        return type to accommodate different data types for the fields.

        Args:
            field_name (str): A string representing the name of the field who
                        needs to be retrieved.

        Returns:
            Optional[FieldModel]: The field corresponding to the
                specified name.
        """
        return self.fields.get(field_name)

    def get_inputs(self) -> dict[str, FieldModel]:
        """
        Retrieve the dictionary of input fields associated with the object.

        Returns:
            dict[str, FieldModel]: Dictionary containing field names as
                keys and their corresponding FieldModel instances as values
        """
        return self.fields

    def remove(self, field_name: str) -> Optional[FieldModel]:
        """
        Removes the specified field from the instance or collection.

        This method is used to delete a specific field identified by
        its name. It ensures the designated field is removed entirely
        from the relevant data structure. No value is returned upon
        successful execution.

        Args:
            field_name (str): The name of the field to be removed.

        Returns:
            Any: The value of the removed field, if any.
        """
        return self.fields.pop(field_name, None)

    def count(self) -> int:
        """
        Counts the total number of elements in the collection.

        This method returns the total count of elements stored within the
        underlying data structure, providing a quick way to ascertain the
        size or number of entries available.

        Returns:
            int: The total number of elements in the collection.
        """
        return len(self.fields)

    def replace(
        self,
        name: str,
        required: bool = False,
        default: Any = None,
        fallback: Any = None,
        filters: Optional[list[BaseFilter]] = None,
        validators: Optional[list[BaseValidator]] = None,
        steps: Optional[list[Union[BaseFilter, BaseValidator]]] = None,
        external_api: Optional[ExternalApiConfig] = None,
        copy: Optional[str] = None,
    ) -> None:
        """
        Replaces a field in the input filter.

        Args:
             name (str): The name of the field.

            required (Optional[bool]): Whether the field is required.

            default (Optional[Any]): The default value of the field.

            fallback (Optional[Any]): The fallback value of the field, if
                validations fails or field None, although it is required.

            filters (Optional[list[BaseFilter]]): The filters to apply to
                the field value.

            validators (Optional[list[BaseValidator]]): The validators to
                apply to the field value.

            steps (Optional[list[Union[BaseFilter, BaseValidator]]]): Allows
                to apply multiple filters and validators in a specific order.

            external_api (Optional[ExternalApiConfig]): Configuration for an
                external API call.

            copy (Optional[str]): The name of the field to copy the value
                from.
        """
        self.fields[name] = FieldModel(
            required,
            default,
            fallback,
            filters or [],
            validators or [],
            steps or [],
            external_api,
            copy,
        )

    def add_global_filter(self, filter: BaseFilter) -> None:
        """
        Add a global filter to be applied to all fields.

        Args:
            filter: The filter to add.
        """
        warnings.warn(
            "Using 'add_global_filter' is deprecated, use 'global_filter()' "
            "instead. https://leandercs.github.io/flask-inputfilter"
            "/options/declarative_api.html",
            DeprecationWarning,
            stacklevel=2,
        )
        self.global_filters.append(filter)

    def get_global_filters(self) -> list[BaseFilter]:
        """
        Retrieve all global filters associated with this InputFilter instance.

        This method returns a list of BaseFilter instances that have been
        added as global filters. These filters are applied universally to
        all fields during data processing.

        Returns:
            list[BaseFilter]: A list of global filters.
        """
        return self.global_filters

    def clear(self) -> None:
        """
        Resets all fields of the InputFilter instance to their initial empty
        state.

        This method clears the internal storage of fields, conditions, filters,
        validators, and data, effectively resetting the object as if it were
        newly initialized.
        """
        self.fields.clear()
        self.conditions.clear()
        self.global_filters.clear()
        self.global_validators.clear()
        self.data.clear()
        self.validated_data.clear()
        self.errors.clear()

    def merge(self, other: InputFilter) -> None:
        """
        Merges another InputFilter instance intelligently into the current
        instance.

        - Fields with the same name are merged recursively if possible,
            otherwise overwritten.
        - Conditions are combined and duplicated.
        - Global filters and validators are merged without duplicates.

        Args:
            other (InputFilter): The InputFilter instance to merge.
        """
        if not isinstance(other, InputFilter):
            raise TypeError(
                "Can only merge with another InputFilter instance."
            )

        DataMixin.merge_input_filters(self, other)

    def set_model(self, model_class: Type[T]) -> None:
        """
        Set the model class for serialization.

        Args:
            model_class (Type[T]): The class to use for serialization.
        """
        self.model_class = model_class

    def _serialize(self) -> Union[dict[str, Any], T]:
        """
        Serialize the validated data. If a model class is set, returns an
        instance of that class, otherwise returns the raw validated data.

        Returns:
            Union[dict[str, Any], T]: The serialized data.
        """
        if self.model_class is None:
            return self.validated_data

        try:
            return self.model_class(**self.validated_data)
        except TypeError:
            pass

        if dataclasses.is_dataclass(self.model_class):
            field_names = {
                f.name for f in dataclasses.fields(self.model_class)
            }
        elif hasattr(self.model_class, "__fields__"):
            field_names = set(self.model_class.__fields__.keys())
        elif hasattr(self.model_class, "__annotations__"):
            field_names = set(self.model_class.__annotations__.keys())
        else:
            sig = inspect.signature(self.model_class.__init__)
            field_names = set(sig.parameters.keys()) - {"self"}

        filtered_data = {
            k: v for k, v in self.validated_data.items() if k in field_names
        }

        return self.model_class(**filtered_data)

    def add_global_validator(self, validator: BaseValidator) -> None:
        """
        Add a global validator to be applied to all fields.

        Args:
            validator (BaseValidator): The validator to add.
        """
        warnings.warn(
            "Using 'add_global_validator' is deprecated, use "
            "'global_validator()' instead. https://leandercs.github.io"
            "/flask-inputfilter/options/declarative_api.html",
            DeprecationWarning,
            stacklevel=2,
        )
        self.global_validators.append(validator)

    def get_global_validators(self) -> list[BaseValidator]:
        """
        Retrieve all global validators associated with this InputFilter
        instance.

        This method returns a list of BaseValidator instances that have been
        added as global validators. These validators are applied universally
        to all fields during validation.

        Returns:
            list[BaseValidator]: A list of global validators.
        """
        return self.global_validators

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from flask import Response, g, request

from flask_inputfilter.conditions import BaseCondition
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import BaseFilter
from flask_inputfilter.mixins import ExternalApiMixin, FieldMixin
from flask_inputfilter.models import ExternalApiConfig, FieldModel
from flask_inputfilter.validators import BaseValidator

T = TypeVar("T")


class InputFilter:
    """Base class for all input filters."""

    def __init__(self, methods: Optional[List[str]] = None) -> None:
        self.methods: List[str] = methods or [
            "GET",
            "POST",
            "PATCH",
            "PUT",
            "DELETE",
        ]
        self.fields: Dict[str, FieldModel] = {}
        self.conditions: List[BaseCondition] = []
        self.global_filters: List[BaseFilter] = []
        self.global_validators: List[BaseValidator] = []
        self.data: Dict[str, Any] = {}
        self.validated_data: Dict[str, Any] = {}
        self.errors: Dict[str, str] = {}
        self.model_class: Optional[Type[T]] = None

    def isValid(self) -> bool:
        """
        Checks if the object's state or its attributes meet certain conditions
        to be considered valid. This function is typically used to ensure that
        the current state complies with specific requirements or rules.

        Returns:
            bool: Returns True if the state or attributes of the object fulfill
                all required conditions; otherwise, returns False.
        """
        import warnings

        warnings.warn(
            "isValid() is deprecated, use is_valid() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.is_valid()

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
    ) -> Callable[
        [Any],
        Callable[
            [tuple[Any, ...], Dict[str, Any]],
            Union[Response, tuple[Any, Dict[str, Any]]],
        ],
    ]:
        """
        Decorator for validating input data in routes.

        Args:
            cls

        Returns:
            Callable[
                [Any],
                Callable[
                    [tuple[Any, ...], Dict[str, Any]],
                    Union[Response, tuple[Any, Dict[str, Any]]],
                ],
            ]
        """

        def decorator(
            f: Callable,
        ) -> Callable[[Any, Any], Union[Response, tuple[Any, Dict[str, Any]]]]:
            """
            Decorator function to validate input data for a Flask route.

            Args:
                f (Callable): The Flask route function to be decorated.

            Returns:
                Callable[
                    [Any, Any],
                    Union[
                        Response,
                        tuple[Any, Dict[str, Any]]
                    ]
                ]: The wrapped function with input validation.
            """

            def wrapper(
                *args, **kwargs
            ) -> Union[Response, tuple[Any, Dict[str, Any]]]:
                """
                Wrapper function to handle input validation and error handling
                for the decorated route function.

                Args:
                    *args: Positional arguments for the route function.
                    **kwargs: Keyword arguments for the route function.

                Returns:
                    Union[Response, tuple[Any, Dict[str, Any]]]: The response
                        from the route function or an error response.
                """
                input_filter = cls()
                if request.method not in input_filter.methods:
                    return Response(status=405, response="Method Not Allowed")

                data = request.json if request.is_json else request.args

                try:
                    kwargs = kwargs or {}

                    input_filter.data = {**data, **kwargs}

                    g.validated_data = input_filter.validateData()

                except ValidationError as e:
                    return Response(
                        status=400,
                        response=json.dumps(e.args[0]),
                        mimetype="application/json",
                    )

                except Exception:
                    logging.getLogger(__name__).exception(
                        "An unexpected exception occurred while "
                        "validating input data.",
                    )
                    return Response(status=500)

                return f(*args, **kwargs)

            return wrapper

        return decorator

    def validateData(
        self, data: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], Type[T]]:
        """
        Validates input data against defined field rules, including applying
        filters, validators, custom logic steps, and fallback mechanisms. The
        validation process also ensures the required fields are handled
        appropriately and conditions are checked after processing.

        Args:
            data (Dict[str, Any]): A dictionary containing the input data to
                be validated where keys represent field names and values
                represent the corresponding data.

        Returns:
            Union[Dict[str, Any], Type[T]]: A dictionary containing the
                validated data with any modifications, default values,
                or processed values as per the defined validation rules.

        Raises:
            Any errors raised during external API calls, validation, or
                logical steps execution of the respective fields or conditions
                will propagate without explicit handling here.
        """
        import warnings

        warnings.warn(
            "validateData() is deprecated, use validate_data() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.validate_data(data)

    def validate_data(
        self, data: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], Type[T]]:
        """
        Validates input data against defined field rules, including applying
        filters, validators, custom logic steps, and fallback mechanisms. The
        validation process also ensures the required fields are handled
        appropriately and conditions are checked after processing.

        Args:
            data (Dict[str, Any]): A dictionary containing the input data to
                be validated where keys represent field names and values
                represent the corresponding data.

        Returns:
            Union[Dict[str, Any], Type[T]]: A dictionary containing the
                validated data with any modifications, default values,
                or processed values as per the defined validation rules.

        Raises:
            Any errors raised during external API calls, validation, or
                logical steps execution of the respective fields or conditions
                will propagate without explicit handling here.
        """
        data = data or self.data
        errors = {}

        for field_name, field_info in self.fields.items():
            value = data.get(field_name)

            required = field_info.required
            default = field_info.default
            fallback = field_info.fallback
            filters = field_info.filters + self.global_filters
            validators = field_info.validators + self.global_validators
            steps = field_info.steps
            external_api = field_info.external_api
            copy = field_info.copy

            try:
                if copy:
                    value = self.validated_data.get(copy)

                if external_api:
                    value = ExternalApiMixin.call_external_api(
                        external_api, fallback, self.validated_data
                    )

                value = FieldMixin.apply_filters(filters, value)
                value = (
                    FieldMixin.validate_field(validators, fallback, value)
                    or value
                )
                value = FieldMixin.apply_steps(steps, fallback, value) or value
                value = FieldMixin.check_for_required(
                    field_name, required, default, fallback, value
                )

                self.validated_data[field_name] = value

            except ValidationError as e:
                errors[field_name] = str(e)

        try:
            FieldMixin.check_conditions(self.conditions, self.validated_data)
        except ValidationError as e:
            errors["_condition"] = str(e)

        if errors:
            raise ValidationError(errors)

        if self.model_class is not None:
            return self.serialize()

        return self.validated_data

    def addCondition(self, condition: BaseCondition) -> None:
        """
        Add a condition to the input filter.

        Args:
            condition (BaseCondition): The condition to add.
        """
        import warnings

        warnings.warn(
            "addCondition() is deprecated, use add_condition() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.add_condition(condition)

    def add_condition(self, condition: BaseCondition) -> None:
        """
        Add a condition to the input filter.

        Args:
            condition (BaseCondition): The condition to add.
        """
        self.conditions.append(condition)

    def getConditions(self) -> List[BaseCondition]:
        """
        Retrieve the list of all registered conditions.

        This function provides access to the conditions that have been
        registered and stored. Each condition in the returned list
        is represented as an instance of the BaseCondition type.

        Returns:
            List[BaseCondition]: A list containing all currently registered
                instances of BaseCondition.
        """
        import warnings

        warnings.warn(
            "getConditions() is deprecated, use get_conditions() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_conditions()

    def get_conditions(self) -> List[BaseCondition]:
        """
        Retrieve the list of all registered conditions.

        This function provides access to the conditions that have been
        registered and stored. Each condition in the returned list
        is represented as an instance of the BaseCondition type.

        Returns:
            List[BaseCondition]: A list containing all currently registered
                instances of BaseCondition.
        """
        return self.conditions

    def setData(self, data: Dict[str, Any]) -> None:
        """
        Filters and sets the provided data into the object's internal storage,
        ensuring that only the specified fields are considered and their values
        are processed through defined filters.

        Parameters:
            data (Dict[str, Any]):
                The input dictionary containing key-value pairs where keys
                represent field names and values represent the associated
                data to be filtered and stored.
        """
        import warnings

        warnings.warn(
            "setData() is deprecated, use set_data() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.set_data(data)

    def set_data(self, data: Dict[str, Any]) -> None:
        """
        Filters and sets the provided data into the object's internal storage,
        ensuring that only the specified fields are considered and their values
        are processed through defined filters.

        Parameters:
            data (Dict[str, Any]):
                The input dictionary containing key-value pairs where keys
                represent field names and values represent the associated
                data to be filtered and stored.
        """
        self.data = {}
        for field_name, field_value in data.items():
            if field_name in self.fields:
                field_value = FieldMixin.apply_filters(
                    filters=self.fields[field_name].filters,
                    value=field_value,
                )

            self.data[field_name] = field_value

    def getValue(self, name: str) -> Any:
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
        import warnings

        warnings.warn(
            "getValue() is deprecated, use get_value() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_value(name)

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

    def getValues(self) -> Dict[str, Any]:
        """
        Retrieves a dictionary of key-value pairs from the current object. This
        method provides access to the internal state or configuration of the
        object in a dictionary format, where keys are strings and values can be
        of various types depending on the object's design.

        Returns:
            Dict[str, Any]: A dictionary containing string keys and their
                            corresponding values of any data type.
        """
        import warnings

        warnings.warn(
            "getValues() is deprecated, use get_values() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_values()

    def get_values(self) -> Dict[str, Any]:
        """
        Retrieves a dictionary of key-value pairs from the current object. This
        method provides access to the internal state or configuration of the
        object in a dictionary format, where keys are strings and values can be
        of various types depending on the object's design.

        Returns:
            Dict[str, Any]: A dictionary containing string keys and their
                            corresponding values of any data type.
        """
        return self.validated_data

    def getRawValue(self, name: str) -> Any:
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
        import warnings

        warnings.warn(
            "getRawValue() is deprecated, use get_raw_value() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_raw_value(name)

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

    def getRawValues(self) -> Dict[str, Any]:
        """
        Retrieves raw values from a given source and returns them as a
        dictionary.

        This method is used to fetch and return unprocessed or raw data in
        the form of a dictionary where the keys are strings, representing
        the identifiers, and the values are of any data type.

        Returns:
            Dict[str, Any]: A dictionary containing the raw values retrieved.
               The keys are strings representing the identifiers, and the
               values can be of any type, depending on the source
               being accessed.
        """
        import warnings

        warnings.warn(
            "getRawValues() is deprecated, use get_raw_values() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_raw_values()

    def get_raw_values(self) -> Dict[str, Any]:
        """
        Retrieves raw values from a given source and returns them as a
        dictionary.

        This method is used to fetch and return unprocessed or raw data in
        the form of a dictionary where the keys are strings, representing
        the identifiers, and the values are of any data type.

        Returns:
            Dict[str, Any]: A dictionary containing the raw values retrieved.
               The keys are strings representing the identifiers, and the
               values can be of any type, depending on the source
               being accessed.
        """
        if not self.fields:
            return {}

        return {
            field: self.data[field]
            for field in self.fields
            if field in self.data
        }

    def getUnfilteredData(self) -> Dict[str, Any]:
        """
        Fetches unfiltered data from the data source.

        This method retrieves data without any filtering, processing, or
        manipulations applied. It is intended to provide raw data that has
        not been altered since being retrieved from its source. The usage
        of this method should be limited to scenarios where unprocessed data
        is required, as it does not perform any validations or checks.

        Returns:
            Dict[str, Any]: The unfiltered, raw data retrieved from the
                 data source. The return type may vary based on the
                 specific implementation of the data source.
        """
        import warnings

        warnings.warn(
            "getUnfilteredData() is deprecated, use "
            "get_unfiltered_data() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_unfiltered_data()

    def get_unfiltered_data(self) -> Dict[str, Any]:
        """
        Fetches unfiltered data from the data source.

        This method retrieves data without any filtering, processing, or
        manipulations applied. It is intended to provide raw data that has
        not been altered since being retrieved from its source. The usage
        of this method should be limited to scenarios where unprocessed data
        is required, as it does not perform any validations or checks.

        Returns:
            Dict[str, Any]: The unfiltered, raw data retrieved from the
                 data source. The return type may vary based on the
                 specific implementation of the data source.
        """
        return self.data

    def setUnfilteredData(self, data: Dict[str, Any]) -> None:
        """
        Sets unfiltered data for the current instance. This method assigns a
        given dictionary of data to the instance for further processing. It
        updates the internal state using the provided data.

        Parameters:
            data (Dict[str, Any]): A dictionary containing the unfiltered
                data to be associated with the instance.
        """
        import warnings

        warnings.warn(
            "setUnfilteredData() is deprecated, use "
            "set_unfiltered_data() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.set_unfiltered_data(data)

    def set_unfiltered_data(self, data: Dict[str, Any]) -> None:
        """
        Sets unfiltered data for the current instance. This method assigns a
        given dictionary of data to the instance for further processing. It
        updates the internal state using the provided data.

        Parameters:
            data (Dict[str, Any]): A dictionary containing the unfiltered
                data to be associated with the instance.
        """
        self.data = data

    def hasUnknown(self) -> bool:
        """
        Checks whether any values in the current data do not have corresponding
        configurations in the defined fields.

        Returns:
            bool: True if there are any unknown fields; False otherwise.
        """
        import warnings

        warnings.warn(
            "hasUnknown() is deprecated, use has_unknown() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.has_unknown()

    def has_unknown(self) -> bool:
        """
        Checks whether any values in the current data do not have corresponding
        configurations in the defined fields.

        Returns:
            bool: True if there are any unknown fields; False otherwise.
        """
        if not self.data and self.fields:
            return True

        return any(
            field_name not in self.fields.keys()
            for field_name in self.data.keys()
        )

    def getErrorMessage(self, field_name: str) -> Optional[str]:
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
        import warnings

        warnings.warn(
            "getErrorMessage() is deprecated, use get_error_message() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_error_message(field_name)

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

    def getErrorMessages(self) -> Dict[str, str]:
        """
        Retrieves all error messages associated with the fields in the input
        filter.

        This method aggregates and returns a dictionary of error messages
        where the keys represent field names, and the values are their
        respective error messages.

        Returns:
            Dict[str, str]: A dictionary containing field names as keys and
                            their corresponding error messages as values.
        """
        import warnings

        warnings.warn(
            "getErrorMessages() is deprecated, use "
            "get_error_messages() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_error_messages()

    def get_error_messages(self) -> Dict[str, str]:
        """
        Retrieves all error messages associated with the fields in the input
        filter.

        This method aggregates and returns a dictionary of error messages
        where the keys represent field names, and the values are their
        respective error messages.

        Returns:
            Dict[str, str]: A dictionary containing field names as keys and
                            their corresponding error messages as values.
        """
        return self.errors

    def add(
        self,
        name: str,
        required: bool = False,
        default: Any = None,
        fallback: Any = None,
        filters: Optional[List[BaseFilter]] = None,
        validators: Optional[List[BaseValidator]] = None,
        steps: Optional[List[Union[BaseFilter, BaseValidator]]] = None,
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

            filters (Optional[List[BaseFilter]]): The filters to apply to
                the field value.

            validators (Optional[List[BaseValidator]]): The validators to
                apply to the field value.

            steps (Optional[List[Union[BaseFilter, BaseValidator]]]): Allows
                to apply multiple filters and validators in a specific order.

            external_api (Optional[ExternalApiConfig]): Configuration for an
                external API call.

            copy (Optional[str]): The name of the field to copy the value
                from.
        """
        if name in self.fields:
            raise ValueError(f"Field '{name}' already exists.")

        self.fields[name] = FieldModel(
            required=required,
            default=default,
            fallback=fallback,
            filters=filters or [],
            validators=validators or [],
            steps=steps or [],
            external_api=external_api,
            copy=copy,
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

    def getInput(self, field_name: str) -> Optional[FieldModel]:
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
        import warnings

        warnings.warn(
            "getInput() is deprecated, use get_input() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_input(field_name)

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

    def getInputs(self) -> Dict[str, FieldModel]:
        """
        Retrieve the dictionary of input fields associated with the object.

        Returns:
            Dict[str, FieldModel]: Dictionary containing field names as
                keys and their corresponding FieldModel instances as values
        """
        import warnings

        warnings.warn(
            "getInputs() is deprecated, use get_inputs() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_inputs()

    def get_inputs(self) -> Dict[str, FieldModel]:
        """
        Retrieve the dictionary of input fields associated with the object.

        Returns:
            Dict[str, FieldModel]: Dictionary containing field names as
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
        filters: Optional[List[BaseFilter]] = None,
        validators: Optional[List[BaseValidator]] = None,
        steps: Optional[List[Union[BaseFilter, BaseValidator]]] = None,
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

            filters (Optional[List[BaseFilter]]): The filters to apply to
                the field value.

            validators (Optional[List[BaseValidator]]): The validators to
                apply to the field value.

            steps (Optional[List[Union[BaseFilter, BaseValidator]]]): Allows
                to apply multiple filters and validators in a specific order.

            external_api (Optional[ExternalApiConfig]): Configuration for an
                external API call.

            copy (Optional[str]): The name of the field to copy the value
                from.
        """
        self.fields[name] = FieldModel(
            required=required,
            default=default,
            fallback=fallback,
            filters=filters or [],
            validators=validators or [],
            steps=steps or [],
            external_api=external_api,
            copy=copy,
        )

    def addGlobalFilter(self, filter: BaseFilter) -> None:
        """
        Add a global filter to be applied to all fields.

        Args:
            filter: The filter to add.
        """
        import warnings

        warnings.warn(
            "addGlobalFilter() is deprecated, use add_global_filter() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.add_global_filter(filter)

    def add_global_filter(self, filter: BaseFilter) -> None:
        """
        Add a global filter to be applied to all fields.

        Args:
            filter: The filter to add.
        """
        self.global_filters.append(filter)

    def getGlobalFilters(self) -> List[BaseFilter]:
        """
        Retrieve all global filters associated with this InputFilter instance.

        This method returns a list of BaseFilter instances that have been
        added as global filters. These filters are applied universally to
        all fields during data processing.

        Returns:
            List[BaseFilter]: A list of global filters.
        """
        import warnings

        warnings.warn(
            "getGlobalFilters() is deprecated, use "
            "get_global_filters() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_global_filters()

    def get_global_filters(self) -> List[BaseFilter]:
        """
        Retrieve all global filters associated with this InputFilter instance.

        This method returns a list of BaseFilter instances that have been
        added as global filters. These filters are applied universally to
        all fields during data processing.

        Returns:
            List[BaseFilter]: A list of global filters.
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

    def merge(self, other: "InputFilter") -> None:
        """
        Merges another InputFilter instance intelligently into the current
        instance.

        - Fields with the same name are merged recursively if possible,
            otherwise overwritten.
        - Conditions, are combined and duplicated.
        - Global filters and validators are merged without duplicates.

        Args:
            other (InputFilter): The InputFilter instance to merge.
        """
        if not isinstance(other, InputFilter):
            raise TypeError(
                "Can only merge with another InputFilter instance."
            )

        for key, new_field in other.getInputs().items():
            self.fields[key] = new_field

        self.conditions += other.conditions

        for filter in other.global_filters:
            existing_type_map = {
                type(v): i for i, v in enumerate(self.global_filters)
            }
            if type(filter) in existing_type_map:
                self.global_filters[existing_type_map[type(filter)]] = filter
            else:
                self.global_filters.append(filter)

        for validator in other.global_validators:
            existing_type_map = {
                type(v): i for i, v in enumerate(self.global_validators)
            }
            if type(validator) in existing_type_map:
                self.global_validators[
                    existing_type_map[type(validator)]
                ] = validator
            else:
                self.global_validators.append(validator)

    def setModel(self, model_class: Type[T]) -> None:
        """
        Set the model class for serialization.

        Args:
            model_class (Type[T]): The class to use for serialization.
        """
        import warnings

        warnings.warn(
            "setModel() is deprecated, use set_model() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.set_model(model_class)

    def set_model(self, model_class: Type[T]) -> None:
        """
        Set the model class for serialization.

        Args:
            model_class (Type[T]): The class to use for serialization.
        """
        self.model_class = model_class

    def serialize(self) -> Union[Dict[str, Any], T]:
        """
        Serialize the validated data. If a model class is set, returns an
        instance of that class, otherwise returns the raw validated data.

        Returns:
            Union[Dict[str, Any], T]: The serialized data.
        """
        if self.model_class is None:
            return self.validated_data

        return self.model_class(**self.validated_data)

    def addGlobalValidator(self, validator: BaseValidator) -> None:
        """
        Add a global validator to be applied to all fields.

        Args:
            validator (BaseValidator): The validator to add.
        """
        import warnings

        warnings.warn(
            "addGlobalValidator() is deprecated, use "
            "add_global_validator() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.add_global_validator(validator)

    def add_global_validator(self, validator: BaseValidator) -> None:
        """
        Add a global validator to be applied to all fields.

        Args:
            validator (BaseValidator): The validator to add.
        """
        self.global_validators.append(validator)

    def getGlobalValidators(self) -> List[BaseValidator]:
        """
        Retrieve all global validators associated with this InputFilter
        instance.

        This method returns a list of BaseValidator instances that have been
        added as global validators. These validators are applied universally
        to all fields during validation.

        Returns:
            List[BaseValidator]: A list of global validators.
        """
        import warnings

        warnings.warn(
            "getGlobalValidators() is deprecated, use "
            "get_global_validators() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_global_validators()

    def get_global_validators(self) -> List[BaseValidator]:
        """
        Retrieve all global validators associated with this InputFilter
        instance.

        This method returns a list of BaseValidator instances that have been
        added as global validators. These validators are applied universally
        to all fields during validation.

        Returns:
            List[BaseValidator]: A list of global validators.
        """
        return self.global_validators

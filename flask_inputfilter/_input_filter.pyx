# cython: language=c++

import json
import logging
import sys
from typing import Any, Optional, Type, TypeVar, Union

from flask import Response, g, request

from flask_inputfilter.exceptions import ValidationError

from flask_inputfilter.mixins.cimports cimport DataMixin
from flask_inputfilter.models.cimports cimport BaseCondition, BaseFilter, BaseValidator, ExternalApiConfig, FieldModel

from libcpp.vector cimport vector
from libcpp.string cimport string

cdef dict _INTERNED_STRINGS = {
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

cdef extern from "helper.h":
    vector[string] make_default_methods()

T = TypeVar("T")


cdef class InputFilter:
    """
    Base class for all input filters.
    """

    def __cinit__(self) -> None:
        self.methods = make_default_methods()
        self.fields = {}
        self.conditions = []
        self.global_filters = []
        self.global_validators = []
        self.data = {}
        self.validated_data = {}
        self.errors = {}
        self.model_class: Optional[Type[T]] = None

    def __init__(self, methods: Optional[list[str]] = None) -> None:
        if methods is not None:
            self.methods.clear()
            [self.methods.push_back(method.encode()) for method in methods]

    cpdef bint is_valid(self):
        """
        Checks if the object's state or its attributes meet certain
        conditions to be considered valid. This function is typically used to
        ensure that the current state complies with specific requirements or
        rules.

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
    ):
        """
        Decorator for validating input data in routes.

        Args:
            cls

        Returns:
            Callable
        """
        def decorator(
            f,
        ):
            """
            Decorator function to validate input data for a Flask route.

            Args:
                f (Callable): The Flask route function to be decorated.

            Returns:
                Callable[[Any, Any], Union[Response, tuple[Any, dict[str, Any]]]]: The wrapped function with input validation.
            """

            def wrapper(
                *args, **kwargs
            ):
                """
                Wrapper function to handle input validation and
                error handling for the decorated route function.

                Args:
                    *args: Positional arguments for the route function.
                    **kwargs: Keyword arguments for the route function.

                Returns:
                    Union[Response, tuple[Any, dict[str, Any]]]: The response from the route function or an error response.
                """

                cdef InputFilter input_filter = cls()
                cdef string request_method = request.method.encode()
                if not any(request_method == method for method in input_filter.methods):
                    return Response(status=405, response="Method Not Allowed")

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

    cpdef object validate_data(
        self, dict[str, Any] data=None
    ):
        """
        Validates input data against defined field rules.

        Args:
            data: Input data dictionary to validate.

        Returns:
            Validated data dictionary or model instance.

        Raises:
            ValidationError: If validation fails.
        """
        data = data or self.data
        cdef:
            dict[str, str] errors
            dict[str, Any] validated_data

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
        return self.serialize()

    cpdef void add_condition(self, BaseCondition condition):
        """
        Add a condition to the input filter.

        Args:
            condition (BaseCondition): The condition to add.
        """
        self.conditions.append(condition)

    cpdef list get_conditions(self):
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

    cpdef void set_data(self, dict[str, Any] data):
        """
        Filters and sets the provided data into the object's internal
        storage, ensuring that only the specified fields are considered and
        their values are processed through defined filters.

        Parameters:
            data (dict[str, Any]):
                The input dictionary containing key-value pairs where keys
                represent field names and values represent the associated
                data to be filtered and stored.
        """
        self.data = DataMixin.filter_data(data, self.fields, self.global_filters)

    cpdef object get_value(self, str name):
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

    cpdef dict[str, Any] get_values(self):
        """
        Retrieves a dictionary of key-value pairs from the current object.
        This method provides access to the internal state or configuration of
        the object in a dictionary format, where keys are strings and values
        can be of various types depending on the object's design.

        Returns:
            dict[str, Any]: A dictionary containing string keys and their
                            corresponding values of any data type.
        """
        return self.validated_data

    cpdef object get_raw_value(self, str name):
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

    cpdef dict[str, Any] get_raw_values(self):
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

        cdef:
            Py_ssize_t i, n = len(self.fields)
            dict result = {}
            list field_names = list(self.fields.keys())
            str field

        for i in range(n):
            field = field_names[i]
            if field in self.data:
                result[field] = self.data[field]
        return result

    cpdef dict[str, Any] get_unfiltered_data(self):
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

    cpdef void set_unfiltered_data(self, dict[str, Any] data):
        """
        Sets unfiltered data for the current instance. This method assigns a
        given dictionary of data to the instance for further processing. It
        updates the internal state using the provided data.

        **Parameters**:

        - data (dict[str, Any]): A dictionary containing the unfiltered
            data to be associated with the instance.
        """
        self.data = data

    cpdef bint has_unknown(self):
        """
        Checks whether any values in the current data do not have
        corresponding configurations in the defined fields.

        Returns:
            bool: True if there are any unknown fields; False otherwise.
        """
        return DataMixin.has_unknown_fields(self.data, self.fields)

    cpdef str get_error_message(self, str field_name):
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

    cpdef dict[str, str] get_error_messages(self):
        """
        Retrieves all error messages associated with the fields in the
        input filter.

        This method aggregates and returns a dictionary of error messages
        where the keys represent field names, and the values are their
        respective error messages.

        Returns:
            dict[str, str]: A dictionary containing field names as keys and
                            their corresponding error messages as values.
        """
        return self.errors

    cpdef void add(
        self,
        str name,
        bint required=False,
        object default=None,
        object fallback=None,
        list[BaseFilter] filters=None,
        list[BaseValidator] validators=None,
        list[BaseFilter | BaseValidator] steps=None,
        ExternalApiConfig external_api=None,
        str copy=None,
    ) except *:
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

            steps (Optional[list[BaseFilter | BaseValidator]]): Allows 
                to apply multiple filters and validators in a specific order.

            external_api (Optional[ExternalApiConfig]): Configuration for an 
                external API call.

            copy (Optional[str]): The name of the field to copy the value 
                from.
        """
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

    cpdef bint has(self, str field_name):
        """
        This method checks the existence of a specific field within the
        input filter values, identified by its field name. It does not return a
        value, serving purely as a validation or existence check mechanism.

        Args:
            field_name (str): The name of the field to check for existence.

        Returns:
            bool: True if the field exists in the input filter,
                otherwise False.
        """
        return field_name in self.fields

    cpdef FieldModel get_input(self, str field_name):
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

    cpdef dict[str, FieldModel] get_inputs(self):
        """
        Retrieve the dictionary of input fields associated with the object.

        Returns:
            dict[str, FieldModel]: Dictionary containing field names as
                keys and their corresponding FieldModel instances as values
        """
        return self.fields

    cpdef object remove(self, field_name: str):
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

    cpdef int count(self):
        """
        Counts the total number of elements in the collection.

        This method returns the total count of elements stored within the
        underlying data structure, providing a quick way to ascertain the
        size or number of entries available.

        Returns:
            int: The total number of elements in the collection.
        """
        return len(self.fields)

    cpdef void replace(
        self,
        str name,
        bint required=False,
        object default=None,
        object fallback=None,
        list[BaseFilter] filters=None,
        list[BaseValidator] validators=None,
        list[BaseFilter | BaseValidator] steps=None,
        ExternalApiConfig external_api=None,
        str copy=None,
    ):
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

            steps (Optional[list[BaseFilter | BaseValidator]]): Allows 
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

    cpdef void add_global_filter(self, BaseFilter filter):
        """
        Add a global filter to be applied to all fields.

        Args:
            filter: The filter to add.
        """
        self.global_filters.append(filter)

    cpdef list[BaseFilter] get_global_filters(self):
        """
        Retrieve all global filters associated with this InputFilter instance.

        This method returns a list of BaseFilter instances that have been
        added as global filters. These filters are applied universally to
        all fields during data processing.

        Returns:
            list[BaseFilter]: A list of global filters.
        """
        return self.global_filters

    cpdef void clear(self):
        """
        Resets all fields of the InputFilter instance to
        their initial empty state.

        This method clears the internal storage of fields,
        conditions, filters, validators, and data, effectively
        resetting the object as if it were newly initialized.
        """
        self.fields.clear()
        self.conditions.clear()
        self.global_filters.clear()
        self.global_validators.clear()
        self.data.clear()
        self.validated_data.clear()
        self.errors.clear()

    cpdef void merge(self, InputFilter other):
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

        DataMixin.merge_input_filters(self, other)

    cpdef void set_model(self, model_class: Type[T]):
        """
        Set the model class for serialization.

        Args:
            model_class (Type[T]): The class to use for serialization.
        """
        self.model_class = model_class

    cpdef object serialize(self):
        """
        Serialize the validated data. If a model class is set,
        returns an instance of that class, otherwise returns the
        raw validated data.

        Returns:
            Union[dict[str, Any], T]: The serialized data.
        """
        if self.model_class is None:
            return self.validated_data

        return self.model_class(**self.validated_data)

    cpdef void add_global_validator(self, BaseValidator validator):
        """
        Add a global validator to be applied to all fields.

        Args:
            validator (BaseValidator): The validator to add.
        """
        self.global_validators.append(validator)

    cpdef list[BaseValidator] get_global_validators(self):
        """
        Retrieve all global validators associated with this
        InputFilter instance.

        This method returns a list of BaseValidator instances that have been
        added as global validators. These validators are applied universally
        to all fields during validation.

        Returns:
            list[BaseValidator]: A list of global validators.
        """
        return self.global_validators

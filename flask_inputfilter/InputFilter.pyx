import re
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from flask import Response, g, request
from typing_extensions import final

from flask_inputfilter.Condition import BaseCondition
from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Filter import BaseFilter
from flask_inputfilter.Model import ExternalApiConfig, FieldModel
from flask_inputfilter.Validator import BaseValidator

API_PLACEHOLDER_PATTERN = re.compile(r"{{(.*?)}}")


class InputFilter:
    """
    Base class for input filters.
    """

    def __init__(self, methods: Optional[List[str]] = None) -> None:
        self.__methods = methods or ["GET", "POST", "PATCH", "PUT", "DELETE"]
        self.__fields: Dict[str, FieldModel] = {}
        self.__conditions: List[BaseCondition] = []
        self.__global_filters: List[BaseFilter] = []
        self.__global_validators: List[BaseValidator] = []
        self.__data: Dict[str, Any] = {}
        self.__validated_data: Dict[str, Any] = {}
        self.__error_message: str = ""

    @final
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
            name: The name of the field.
            required: Whether the field is required.
            default: The default value of the field.
            fallback: The fallback value of the field, if validations fails
                or field None, although it is required .
            filters: The filters to apply to the field value.
            validators: The validators to apply to the field value.
            steps: Allows to apply multiple filters and validators
                in a specific order.
            external_api: Configuration for an external API call.
            copy: The name of the field to copy the value from.
        """
        self.__fields[name] = FieldModel(
            required=required,
            default=default,
            fallback=fallback,
            filters=filters or [],
            validators=validators or [],
            steps=steps or [],
            external_api=external_api,
            copy=copy,
        )

    @final
    def addCondition(self, condition: BaseCondition) -> None:
        """
        Add a condition to the input filter.

        Args:
            condition: The condition to add.
        """
        self.__conditions.append(condition)

    @final
    def addGlobalFilter(self, filter: BaseFilter) -> None:
        """
        Add a global filter to be applied to all fields.

        Args:
            filter: The filter to add.
        """
        self.__global_filters.append(filter)

    @final
    def addGlobalValidator(self, validator: BaseValidator) -> None:
        """
        Add a global validator to be applied to all fields.

        Args:
            validator: The validator to add.
        """
        self.__global_validators.append(validator)

    @final
    def has(self, field_name: str) -> bool:
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
        return field_name in self.__fields

    @final
    def getInput(self, field_name: str) -> FieldModel:
        """
        Represents a method to retrieve the value of a field by its name.

        This method allows fetching the value of a specific field within the
        object, using its name as a string. It ensures compatibility with
        various field names and provides a generic return type to accommodate
        different data types for the fields.

        Args:
            field_name: A string representing the name of the field whose value
                        needs to be retrieved.

        Returns:
            Any: The value of the field corresponding to the specified name.
        """
        return self.__fields.get(field_name)

    @final
    def getInputs(self) -> Dict[str, FieldModel]:
        """
        Retrieve the dictionary of input fields associated with the object.

        Returns:
            Dict[str, FieldModel]: Dictionary containing field names as
                keys and their corresponding FieldModel instances as values
        """
        return self.__fields

    @final
    def remove(self, field_name: str) -> Any:
        """
        Removes the specified field from the instance or collection.

        This method is used to delete a specific field identified by
        its name. It ensures the designated field is removed entirely
        from the relevant data structure. No value is returned upon
        successful execution.

        Args:
            field_name: The name of the field to be removed.

        Returns:
            Any: The value of the removed field, if any.
        """
        return self.__fields.pop(field_name, None)

    @final
    def count(self) -> int:
        """
        Counts the total number of elements in the collection.

        This method returns the total count of elements stored within the
        underlying data structure, providing a quick way to ascertain the
        size or number of entries available.

        Returns:
            int: The total number of elements in the collection.
        """
        return len(self.__fields)

    @final
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
            name: The name of the field.
            required: Whether the field is required.
            default: The default value of the field.
            fallback: The fallback value of the field, if validations fails
                or field None, although it is required .
            filters: The filters to apply to the field value.
            validators: The validators to apply to the field value.
            steps: Allows to apply multiple filters and validators
                in a specific order.
            external_api: Configuration for an external API call.
            copy: The name of the field to copy the value from.
        """
        self.__fields[name] = FieldModel(
            required=required,
            default=default,
            fallback=fallback,
            filters=filters or [],
            validators=validators or [],
            steps=steps or [],
            external_api=external_api,
            copy=copy,
        )

    @final
    def setData(self, data: Dict[str, Any]) -> None:
        """
        Filters and sets the provided data into the object's internal
        storage, ensuring that only the specified fields are considered and
        their values are processed through defined filters.

        Parameters:
            data:
                The input dictionary containing key-value pairs where keys
                represent field names and values represent the associated
                data to be filtered and stored.
        """
        filtered_data = {}
        for field_name, field_value in data.items():
            if field_name in self.__fields:
                filtered_data[field_name] = self.__applyFilters(
                    filters=self.__fields[field_name].filters,
                    value=field_value,
                )
            else:
                filtered_data[field_name] = field_value

        self.__data = filtered_data

    @final
    def getErrorMessage(self) -> str:
        """
        Retrieves and returns a predefined error message.

        This method is intended to provide a consistent error message
        to be used across the application when an error occurs. The
        message is predefined and does not accept any parameters.
        The exact content of the error message may vary based on
        specific implementation, but it is designed to convey meaningful
        information about the nature of an error.

        Returns:
            str: A string representing the predefined error message.
        """
        return self.__error_message

    @final
    def getValue(self, name: str) -> Any:
        """
        This method retrieves a value associated with the provided name. It
        searches for the value based on the given identifier and returns the
        corresponding result. If no value is found, it typically returns a
        default or fallback output. The method aims to provide flexibility in
        retrieving data without explicitly specifying the details of the
        underlying implementation.

        Args:
            name: A string that represents the identifier for which the
                 corresponding value is being retrieved. It is used to perform
                 the lookup.

        Returns:
            Any: The retrieved value associated with the given name. The
                 specific type of this value is dependent on the
                 implementation and the data being accessed.
        """
        return self.__validated_data.get(name)

    @final
    def getValues(self) -> Dict[str, Any]:
        """
        Retrieves a dictionary of key-value pairs from the current object.
        This method provides access to the internal state or configuration of
        the object in a dictionary format, where keys are strings and values
        can be of various types depending on the object’s design.

        Returns:
            Dict[str, Any]: A dictionary containing string keys and their
                            corresponding values of any data type.
        """
        return self.__validated_data

    @final
    def getRawValue(self, name: str) -> Any:
        """
        Fetches the raw value associated with the provided key.

        This method is used to retrieve the underlying value linked to the
        given key without applying any transformations or validations. It
        directly fetches the raw stored value and is typically used in
        scenarios where the raw data is needed for processing or debugging
        purposes.

        Args:
            name: The name of the key whose raw value is to be retrieved.

        Returns:
            Any: The raw value associated with the provided key.
        """
        return self.__data.get(name) if name in self.__data else None

    @final
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
        if not self.__fields:
            return {}

        return {
            field: self.__data[field]
            for field in self.__fields
            if field in self.__data
        }

    @final
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
        return self.__data

    @final
    def setUnfilteredData(self, data: Dict[str, Any]) -> None:
        """
        Sets unfiltered data for the current instance. This method assigns a
        given dictionary of data to the instance for further processing. It
        updates the internal state using the provided data.

        Parameters:
            data: A dictionary containing the unfiltered
                data to be associated with the instance.
        """
        self.__data = data

    @final
    def hasUnknown(self) -> bool:
        """
        Checks whether any values in the current data do not have
        corresponding configurations in the defined fields.

        Returns:
            bool: True if there are any unknown fields; False otherwise.
        """
        if not self.__data and self.__fields:
            return True
        return any(
            field_name not in self.__fields.keys()
            for field_name in self.__data.keys()
        )

    @final
    def merge(self, other: "InputFilter") -> None:
        """
        Merges another InputFilter instance intelligently into the current
        instance.

        - Fields with the same name are merged recursively if possible,
            otherwise overwritten.
        - Conditions are combined and deduplicated.
        - Global filters and validators are merged without duplicates.

        Args:
            other (InputFilter): The InputFilter instance to merge.
        """
        if not isinstance(other, InputFilter):
            raise TypeError(
                "Can only merge with another InputFilter instance."
            )

        for key, new_field in other.getInputs().items():
            if key not in self.__fields:
                self.__fields[key] = new_field
                continue

            existing_field = self.__fields[key]
            if not isinstance(existing_field, InputFilter) or not isinstance(
                new_field, InputFilter
            ):
                self.__fields[key] = new_field

            existing_field.merge(new_field)

        self.__conditions = list(set(self.__conditions + other.__conditions))

        existing_global_filters = set(self.__global_filters)
        for filter in other.__global_filters:
            if filter not in existing_global_filters:
                self.__global_filters.append(filter)
                existing_global_filters.add(filter)

        existing_global_validators = set(self.__global_validators)
        for validator in other.__global_validators:
            if validator not in existing_global_validators:
                self.__global_validators.append(validator)
                existing_global_validators.add(validator)

    @final
    def isValid(self) -> bool:
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
            self.validateData(self.__data)

        except (ValidationError, Exception) as e:
            self.__error_message = str(e)
            return False

        return True

    @final
    def validateData(
        self, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
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
            Dict[str, Any]: A dictionary containing the validated data with
                any modifications, default values, or processed values as
                per the defined validation rules.

        Raises:
            Any errors raised during external API calls, validation, or
                logical steps execution of the respective fields or conditions
                will propagate without explicit handling here.
        """
        validated_data = self.__validated_data
        data = data or self.__data

        for field_name, field_info in self.__fields.items():
            value = data.get(field_name)

            required = field_info.required
            default = field_info.default
            fallback = field_info.fallback
            filters = field_info.filters
            validators = field_info.validators
            steps = field_info.steps
            external_api = field_info.external_api
            copy = field_info.copy

            if copy:
                value = validated_data.get(copy)

            if external_api:
                value = self.__callExternalApi(
                    external_api, fallback, validated_data
                )

            value = self.__applyFilters(filters, value)

            value = self.__validateField(validators, fallback, value) or value

            value = self.__applySteps(steps, fallback, value) or value

            value = self.__checkForRequired(
                field_name, required, default, fallback, value
            )

            validated_data[field_name] = value

        self.__checkConditions(validated_data)

        self.__validated_data = validated_data

        return validated_data

    @classmethod
    @final
    def validate(
        cls,
    ) -> Callable[
        [Any],
        Callable[
            [Tuple[Any, ...], Dict[str, Any]],
            Union[Response, Tuple[Any, Dict[str, Any]]],
        ],
    ]:
        """
        Decorator for validating input data in routes.
        """

        def decorator(
            f,
        ) -> Callable[
            [Tuple[Any, ...], Dict[str, Any]],
            Union[Response, Tuple[Any, Dict[str, Any]]],
        ]:
            def wrapper(
                *args, **kwargs
            ) -> Union[Response, Tuple[Any, Dict[str, Any]]]:
                input_filter = cls()
                if request.method not in input_filter.__methods:
                    return Response(status=405, response="Method Not Allowed")

                data = request.json if request.is_json else request.args

                try:
                    kwargs = kwargs or {}

                    input_filter.__data = {**data, **kwargs}

                    g.validated_data = input_filter.validateData()

                except ValidationError as e:
                    return Response(status=400, response=str(e))

                return f(*args, **kwargs)

            return wrapper

        return decorator

    def __applyFilters(self, filters: List[BaseFilter], value: Any) -> Any:
        """
        Apply filters to the field value.
        """
        if value is None:
            return value

        for filter_ in self.__global_filters + filters:
            value = filter_.apply(value)

        return value

    def __validateField(
        self, validators: List[BaseValidator], fallback: Any, value: Any
    ) -> None:
        """
        Validate the field value.
        """
        if value is None:
            return

        try:
            for validator in self.__global_validators + validators:
                validator.validate(value)
        except ValidationError:
            if fallback is None:
                raise

            return fallback

    @staticmethod
    def __applySteps(
        steps: List[Union[BaseFilter, BaseValidator]],
        fallback: Any,
        value: Any,
    ) -> Any:
        """
        Apply multiple filters and validators in a specific order.
        """
        if value is None:
            return

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

    def __callExternalApi(
        self, config: ExternalApiConfig, fallback: Any, validated_data: dict
    ) -> Optional[Any]:
        """
        Makes a call to an external API using provided configuration and
        returns the response.

        Summary:
        The function constructs a request based on the given API
        configuration and validated data, including headers, parameters,
        and other request settings. It utilizes the `requests` library
        to send the API call and processes the response. If a fallback
        value is supplied, it is returned in case of any failure during
        the API call. If no fallback is provided, a validation error is
        raised.

        Parameters:
            config:
                An object containing the configuration details for the
                external API call, such as URL, headers, method, and API key.
            fallback:
                The value to be returned in case the external API call fails.
            validated_data:
                The dictionary containing data used to replace placeholders
                in the URL and parameters of the API request.

        Returns:
            Optional[Any]:
                The JSON-decoded response from the API, or the fallback
                value if the call fails and a fallback is provided.

        Raises:
            ValidationError
                Raised if the external API call does not succeed and no
                fallback value is provided.
        """
        import requests

        requestData = {
            "headers": {},
            "params": {},
        }

        if config.api_key:
            requestData["headers"]["Authorization"] = (
                f"Bearer " f"{config.api_key}"
            )

        if config.headers:
            requestData["headers"].update(config.headers)

        if config.params:
            requestData["params"] = self.__replacePlaceholdersInParams(
                config.params, validated_data
            )

        requestData["url"] = self.__replacePlaceholders(
            config.url, validated_data
        )
        requestData["method"] = config.method

        try:
            response = requests.request(**requestData)

            if response.status_code != 200:
                raise ValidationError(
                    f"External API call failed with "
                    f"status code {response.status_code}"
                )

            result = response.json()

            data_key = config.data_key
            if data_key:
                return result.get(data_key)

            return result
        except Exception as e:
            if fallback is None:
                self.__error_message = str(e)

                raise ValidationError(
                    f"External API call failed for field "
                    f"'{config.data_key}'."
                )

            return fallback

    @staticmethod
    def __replacePlaceholders(value: str, validated_data: dict) -> str:
        """
        Replace all placeholders, marked with '{{ }}' in value
        with the corresponding values from validated_data.
        """
        return API_PLACEHOLDER_PATTERN.sub(
            lambda match: str(validated_data.get(match.group(1))),
            value,
        )

    def __replacePlaceholdersInParams(
        self, params: dict, validated_data: dict
    ) -> dict:
        """
        Replace all placeholders in params with the corresponding
        values from validated_data.
        """
        return {
            key: self.__replacePlaceholders(value, validated_data)
            if isinstance(value, str)
            else value
            for key, value in params.items()
        }

    @staticmethod
    def __checkForRequired(
        field_name: str,
        required: bool,
        default: Any,
        fallback: Any,
        value: Any,
    ) -> Any:
        """
        Determine the value of the field, considering the required and
        fallback attributes.

        If the field is not required and no value is provided, the default
        value is returned. If the field is required and no value is provided,
        the fallback value is returned. If no of the above conditions are met,
        a ValidationError is raised.
        """
        if value is not None:
            return value

        if not required:
            return default

        if fallback is not None:
            return fallback

        raise ValidationError(f"Field '{field_name}' is required.")

    def __checkConditions(self, validated_data: dict) -> None:
        for condition in self.__conditions:
            if not condition.check(validated_data):
                raise ValidationError(f"Condition '{condition}' not met.")

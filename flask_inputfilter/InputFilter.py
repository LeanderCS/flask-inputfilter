import json
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from flask import Response, g, request
from typing_extensions import final

from flask_inputfilter.Condition import BaseCondition
from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Filter import BaseFilter
from flask_inputfilter.Mixin import (
    ConditionMixin,
    DataMixin,
    ErrorHandlingMixin,
    ExternalApiMixin,
    FieldMixin,
    FilterMixin,
    ModelMixin,
    ValidationMixin,
)
from flask_inputfilter.Model import FieldModel
from flask_inputfilter.Validator import BaseValidator

T = TypeVar("T")


class InputFilter(
    ConditionMixin,
    DataMixin,
    ErrorHandlingMixin,
    ExternalApiMixin,
    FieldMixin,
    FilterMixin,
    ModelMixin,
    ValidationMixin,
):
    """
    Base class for input filters.
    """

    __slots__ = (
        "__methods",
        "_fields",
        "_conditions",
        "_global_filters",
        "_global_validators",
        "_data",
        "_validated_data",
        "_errors",
        "_model_class",
    )

    def __init__(self, methods: Optional[List[str]] = None) -> None:
        self.__methods = methods or ["GET", "POST", "PATCH", "PUT", "DELETE"]
        self._fields: Dict[str, FieldModel] = {}
        self._conditions: List[BaseCondition] = []
        self._global_filters: List[BaseFilter] = []
        self._global_validators: List[BaseValidator] = []
        self._data: Dict[str, Any] = {}
        self._validated_data: Dict[str, Any] = {}
        self._errors: Dict[str, str] = {}
        self._model_class: Optional[Type[T]] = None

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
            self.validateData(self._data)

        except ValidationError as e:
            self._errors = e.args[0]
            return False

        return True

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

                    input_filter._data = {**data, **kwargs}

                    validated_data = input_filter.validateData()

                    if input_filter._model_class is not None:
                        validated_data = input_filter.serialize()

                    g.validated_data = validated_data

                except ValidationError as e:
                    return Response(
                        status=400,
                        response=json.dumps(e.args[0]),
                        mimetype="application/json",
                    )

                return f(*args, **kwargs)

            return wrapper

        return decorator

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
        validated_data = self._validated_data
        data = data or self._data
        errors = {}

        for field_name, field_info in self._fields.items():
            value = data.get(field_name)

            required = field_info.required
            default = field_info.default
            fallback = field_info.fallback
            filters = field_info.filters
            validators = field_info.validators
            steps = field_info.steps
            external_api = field_info.external_api
            copy = field_info.copy

            try:
                if copy:
                    value = validated_data.get(copy)

                if external_api:
                    value = self._ExternalApiMixin__callExternalApi(
                        external_api, fallback, validated_data
                    )

                value = self._FilterMixin__applyFilters(filters, value)
                value = (
                    self._ValidationMixin__validateField(
                        validators, fallback, value
                    )
                    or value
                )
                value = (
                    self._FieldMixin__applySteps(steps, fallback, value)
                    or value
                )
                value = self._FieldMixin__checkForRequired(
                    field_name, required, default, fallback, value
                )

                validated_data[field_name] = value

            except ValidationError as e:
                errors[field_name] = str(e)

        try:
            self._ConditionMixin__checkConditions(validated_data)
        except ValidationError as e:
            errors["_condition"] = str(e)

        if errors:
            raise ValidationError(errors)

        self._validated_data = validated_data
        return validated_data

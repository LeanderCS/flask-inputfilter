from typing import Any, Dict, List, Optional, Union

from typing_extensions import final

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Filter import BaseFilter
from flask_inputfilter.Mixin import BaseMixin
from flask_inputfilter.Model import ExternalApiConfig, FieldModel
from flask_inputfilter.Validator import BaseValidator


class FieldMixin(BaseMixin):
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
        self._fields[name] = FieldModel(
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
        return field_name in self._fields

    @final
    def getInput(self, field_name: str) -> Optional[FieldModel]:
        """
        Represents a method to retrieve a field by its name.

        This method allows fetching the configuration of a specific field
        within the object, using its name as a string. It ensures
        compatibility with various field names and provides a generic
        return type to accommodate different data types for the fields.

        Args:
            field_name: A string representing the name of the field who
                        needs to be retrieved.

        Returns:
            Optional[FieldModel]: The field corresponding to the
                specified name.
        """
        return self._fields.get(field_name)

    @final
    def getInputs(self) -> Dict[str, FieldModel]:
        """
        Retrieve the dictionary of input fields associated with the object.

        Returns:
            Dict[str, FieldModel]: Dictionary containing field names as
                keys and their corresponding FieldModel instances as values
        """
        return self._fields

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
        return self._fields.pop(field_name, None)

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
        return len(self._fields)

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
        self._fields[name] = FieldModel(
            required=required,
            default=default,
            fallback=fallback,
            filters=filters or [],
            validators=validators or [],
            steps=steps or [],
            external_api=external_api,
            copy=copy,
        )

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

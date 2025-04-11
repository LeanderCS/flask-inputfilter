from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from typing_extensions import final

from flask_inputfilter.Mixin import BaseMixin

if TYPE_CHECKING:
    from flask_inputfilter import InputFilter

T = TypeVar("T")


class ModelMixin(BaseMixin):
    @final
    def clear(self) -> None:
        """
        Resets all fields of the InputFilter instance to
        their initial empty state.

        This method clears the internal storage of fields,
        conditions, filters, validators, and data, effectively
        resetting the object as if it were newly initialized.
        """
        self._fields.clear()
        self._conditions.clear()
        self._global_filters.clear()
        self._global_validators.clear()
        self._data.clear()
        self._validated_data.clear()
        self._errors.clear()

    @final
    def merge(self, other: "InputFilter") -> None:
        """
        Merges another InputFilter instance intelligently into the current
        instance.

        - Fields with the same name are merged recursively if possible,
            otherwise overwritten.
        - Conditions,  are combined and deduplicated.
        - Global filters and validators are merged without duplicates.

        Args:
            other (InputFilter): The InputFilter instance to merge.
        """
        from flask_inputfilter import InputFilter

        if not isinstance(other, InputFilter):
            raise TypeError(
                "Can only merge with another InputFilter instance."
            )

        for key, new_field in other.getInputs().items():
            self._fields[key] = new_field

        self._conditions = self._conditions + other._conditions

        for filter in other._global_filters:
            existing_types = [type(v) for v in self._global_filters]
            if type(filter) in existing_types:
                index = existing_types.index(type(filter))
                self._global_filters[index] = filter

            else:
                self._global_filters.append(filter)

        for validator in other._global_validators:
            existing_types = [type(v) for v in self._global_validators]
            if type(validator) in existing_types:
                index = existing_types.index(type(validator))
                self._global_validators[index] = validator

            else:
                self._global_validators.append(validator)

    @final
    def setModel(self, model_class: Type[T]) -> None:
        """
        Set the model class for serialization.

        Args:
            model_class: The class to use for serialization.
        """
        self._model_class = model_class

    @final
    def serialize(self) -> Union[Dict[str, Any], T]:
        """
        Serialize the validated data. If a model class is set,
        returns an instance of that class, otherwise returns the
        raw validated data.

        Returns:
            Union[Dict[str, Any], T]: The serialized data.
        """
        if self._model_class is None:
            return self._validated_data

        return self._model_class(**self._validated_data)

from __future__ import annotations

import dataclasses
from typing import Any, ClassVar, Optional, Type, TypeVar, Union, _GenericAlias

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator

T = TypeVar("T")


# Compatibility functions for Python 3.7 support
try:
    from typing import get_args, get_origin
except ImportError:
    # Fallback implementations for Python 3.7
    def get_origin(tp: Any) -> Optional[Type[Any]]:
        """
        Get the unsubscripted version of a type.

        This supports typing types like list, dict, etc. and their
        typing_extensions equivalents.
        """
        if isinstance(tp, _GenericAlias):
            return tp.__origin__
        return None

    def get_args(tp: Any) -> tuple[Any, ...]:
        """
        Get type arguments with all substitutions performed.

        For unions, basic types, and special typing forms, returns the type
        arguments. For example, for list[int] returns (int,).
        """
        if isinstance(tp, _GenericAlias):
            return tp.__args__
        return ()


class IsDataclassValidator(BaseValidator):
    """
    Validates that the provided value conforms to a specific dataclass type.

    **Parameters:**

    - **dataclass_type** (*Type[dict]*): The expected dataclass type.
    - **error_message** (*Optional[str]*): Custom error message if
      validation fails.

    **Expected Behavior:**

    Ensures the input is a dictionary and, that all expected keys are present.
    Raises a ``ValidationError`` if the structure does not match.
    All fields in the dataclass are validated against their types, including
    nested dataclasses, lists, and dictionaries.

    **Example Usage:**

    .. code-block:: python

        from dataclasses import dataclass

        @dataclass
        class User:
            id: int
            name: str

        class UserInputFilter(InputFilter):
            user: dict = field(validators=[
                IsDataclassValidator(dataclass_type=User)
            ])
    """

    __slots__ = ("dataclass_type", "error_message")

    _ERROR_TEMPLATES: ClassVar = {
        "not_dict": "The provided value is not a dict instance.",
        "not_dataclass": "'{dataclass_type}' is not a valid dataclass.",
        "missing_field": "Missing required field '{field_name}' in value "
        "'{value}'.",
        "type_mismatch": "Field '{field_name}' in value '{value}' is not of "
        "type '{expected_type}'.",
        "list_type": "Field '{field_name}' in value '{value}' is not a valid "
        "list of '{item_type}'.",
        "list_item": "Item at index {index} in field '{field_name}' is not "
        "of type '{expected_type}'.",
        "dict_type": "Field '{field_name}' in value '{value}' is not a valid "
        "dict with keys of type '{key_type}' and values of type "
        "'{value_type}'.",
        "dict_key": "Key '{key}' in field '{field_name}' is not of type "
        "'{expected_type}'.",
        "dict_value": "Value for key '{key}' in field '{field_name}' is not "
        "of type '{expected_type}'.",
        "union_mismatch": "Field '{field_name}' in value '{value}' does not "
        "match any of the types: {types}.",
        "unsupported_type": "Unsupported type '{field_type}' for field "
        "'{field_name}'.",
    }

    def __init__(
        self,
        dataclass_type: Type[T],
        error_message: Optional[str] = None,
    ) -> None:
        self.dataclass_type = dataclass_type
        self.error_message = error_message

        if not dataclasses.is_dataclass(self.dataclass_type):
            raise ValueError(
                self._format_error(
                    "not_dataclass", dataclass_type=self.dataclass_type
                )
            )

    def _format_error(self, error_type: str, **kwargs: Any) -> str:
        """Format error message using template or custom message."""
        if self.error_message:
            return self.error_message

        template = self._ERROR_TEMPLATES.get(error_type, "Validation error")
        return template.format(**kwargs)

    def validate(self, value: Any) -> None:
        """Validate that value conforms to the dataclass type."""
        self._validate_is_dict(value)

        for field in dataclasses.fields(self.dataclass_type):
            self._validate_field(field, value)

    def _validate_is_dict(self, value: Any) -> None:
        """Ensure value is a dictionary."""
        if not isinstance(value, dict):
            raise ValidationError(self._format_error("not_dict"))

    def _validate_field(
        self, field: dataclasses.Field, value: dict[str, Any]
    ) -> None:
        """Validate a single field of the dataclass."""
        field_name = field.name
        field_type = field.type

        if field_name not in value:
            if not IsDataclassValidator._has_default(field):
                raise ValidationError(
                    self._format_error(
                        "missing_field", field_name=field_name, value=value
                    )
                )
            return

        field_value = value[field_name]
        self._validate_field_type(field_name, field_value, field_type, value)

    @staticmethod
    def _has_default(field: dataclasses.Field) -> bool:
        """Check if a field has a default value."""
        return (
            field.default is not dataclasses.MISSING
            or field.default_factory is not dataclasses.MISSING
        )

    def _validate_field_type(
        self,
        field_name: str,
        field_value: Any,
        field_type: Type,
        parent_value: dict[str, Any],
    ) -> None:
        """Validate that a field value matches its expected type."""
        origin = get_origin(field_type)

        if origin is not None:
            self._validate_generic_type(
                field_name, field_value, field_type, origin, parent_value
            )
        elif dataclasses.is_dataclass(field_type):
            IsDataclassValidator._validate_nested_dataclass(
                field_value, field_type
            )
        else:
            self._validate_simple_type(
                field_name, field_value, field_type, parent_value
            )

    def _validate_generic_type(
        self,
        field_name: str,
        field_value: Any,
        field_type: Type,
        origin: Type,
        parent_value: dict[str, Any],
    ) -> None:
        """Validate generic types like list[T], dict[K, V], Optional[T]."""
        args = get_args(field_type)

        validators = {
            list: self._validate_list_type,
            dict: self._validate_dict_type,
            Union: self._validate_union_type,
        }

        validator = validators.get(origin)
        if validator:
            validator(field_name, field_value, args, parent_value)
        else:
            raise ValidationError(
                self._format_error(
                    "unsupported_type",
                    field_type=field_type,
                    field_name=field_name,
                )
            )

    def _validate_list_type(
        self,
        field_name: str,
        field_value: Any,
        args: tuple[Type, ...],
        parent_value: dict[str, Any],
    ) -> None:
        """Validate list[T] type."""
        if not isinstance(field_value, list):
            raise ValidationError(
                self._format_error(
                    "list_type",
                    field_name=field_name,
                    value=parent_value,
                    item_type=args[0],
                )
            )

        item_type = args[0]
        for i, item in enumerate(field_value):
            if not isinstance(item, item_type):
                raise ValidationError(
                    self._format_error(
                        "list_item",
                        index=i,
                        field_name=field_name,
                        expected_type=item_type,
                    )
                )

    def _validate_dict_type(
        self,
        field_name: str,
        field_value: Any,
        args: tuple[Type, ...],
        parent_value: dict[str, Any],
    ) -> None:
        """Validate dict[K, V] type."""
        if not isinstance(field_value, dict):
            raise ValidationError(
                self._format_error(
                    "dict_type",
                    field_name=field_name,
                    value=parent_value,
                    key_type=args[0],
                    value_type=args[1],
                )
            )

        key_type, value_type = args[0], args[1]
        for k, v in field_value.items():
            if not isinstance(k, key_type):
                raise ValidationError(
                    self._format_error(
                        "dict_key",
                        key=k,
                        field_name=field_name,
                        expected_type=key_type,
                    )
                )
            if not isinstance(v, value_type):
                raise ValidationError(
                    self._format_error(
                        "dict_value",
                        key=k,
                        field_name=field_name,
                        expected_type=value_type,
                    )
                )

    def _validate_union_type(
        self,
        field_name: str,
        field_value: Any,
        args: tuple[Type, ...],
        parent_value: dict[str, Any],
    ) -> None:
        """Validate Union types, particularly Optional[T]."""
        if None in args:
            if field_value is None:
                return

            non_none_types = [t for t in args if t is not None]
            if len(non_none_types) == 1:
                expected_type = non_none_types[0]
                if not isinstance(field_value, expected_type):
                    raise ValidationError(
                        self._format_error(
                            "type_mismatch",
                            field_name=field_name,
                            value=parent_value,
                            expected_type=expected_type,
                        )
                    )
                return

        if not any(isinstance(field_value, t) for t in args):
            types_str = ", ".join(str(t) for t in args)
            raise ValidationError(
                self._format_error(
                    "union_mismatch",
                    field_name=field_name,
                    value=parent_value,
                    types=types_str,
                )
            )

    @staticmethod
    def _validate_nested_dataclass(field_value: Any, field_type: Type) -> None:
        """Validate nested dataclass."""
        nested_validator = IsDataclassValidator(field_type)
        nested_validator.validate(field_value)

    def _validate_simple_type(
        self,
        field_name: str,
        field_value: Any,
        field_type: Type,
        parent_value: dict[str, Any],
    ) -> None:
        """Validate simple types like int, str, bool, etc."""
        if not isinstance(field_value, field_type):
            raise ValidationError(
                self._format_error(
                    "type_mismatch",
                    field_name=field_name,
                    value=parent_value,
                    expected_type=field_type,
                )
            )

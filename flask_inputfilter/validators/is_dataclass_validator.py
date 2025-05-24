from __future__ import annotations

import dataclasses
from typing import Any, Optional, Type, TypeVar, Union, _GenericAlias

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator

T = TypeVar("T")


# TODO: Replace with typing.get_origin when Python 3.7 support is dropped.
def get_origin(tp: Any) -> Optional[Type[Any]]:
    """Get the unsubscripted version of a type.

    This supports typing types like List, Dict, etc. and their
    typing_extensions equivalents.
    """
    if isinstance(tp, _GenericAlias):
        return tp.__origin__
    return None


# TODO: Replace with typing.get_args when Python 3.7 support is dropped.
def get_args(tp: Any) -> tuple[Any, ...]:
    """Get type arguments with all substitutions performed.

    For unions, basic types, and special typing forms, returns
    the type arguments. For example, for List[int] returns (int,).
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
            def __init__(self):
                super().__init__()

                self.add('user', validators=[
                    IsDataclassValidator(dataclass_type=User)
                ])
    """

    __slots__ = ("dataclass_type", "error_message")

    def __init__(
        self,
        dataclass_type: Type[T],
        error_message: Optional[str] = None,
    ) -> None:
        self.dataclass_type = dataclass_type
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, dict):
            raise ValidationError(
                self.error_message
                or "The provided value is not a dict instance."
            )

        if not dataclasses.is_dataclass(self.dataclass_type):
            raise ValidationError(
                self.error_message
                or f"'{self.dataclass_type}' is not a valid dataclass."
            )

        for field in dataclasses.fields(self.dataclass_type):
            field_name = field.name
            field_type = field.type
            has_default = (
                field.default is not dataclasses.MISSING
                or field.default_factory is not dataclasses.MISSING
            )

            if field_name not in value:
                if not has_default:
                    raise ValidationError(
                        self.error_message
                        or f"Missing required field '{field_name}' in "
                        f"value '{value}'."
                    )
                continue

            field_value = value[field_name]

            origin = get_origin(field_type)
            args = get_args(field_type)

            if origin is not None:
                if origin is list:
                    if not isinstance(field_value, list) or not all(
                        isinstance(item, args[0]) for item in field_value
                    ):
                        raise ValidationError(
                            self.error_message
                            or f"Field '{field_name}' in value '{value}' is "
                            f"not a valid list of '{args[0]}'."
                        )
                elif origin is dict:
                    if not isinstance(field_value, dict) or not all(
                        isinstance(k, args[0]) and isinstance(v, args[1])
                        for k, v in field_value.items()
                    ):
                        raise ValidationError(
                            self.error_message
                            or f"Field '{field_name}' in value '{value}' is "
                            f"not a valid dict with keys of type "
                            f"'{args[0]}' and values of type '{args[1]}'."
                        )
                elif origin is Union and type(None) in args:
                    if field_value is not None and not isinstance(
                        field_value, args[0]
                    ):
                        raise ValidationError(
                            self.error_message
                            or f"Field '{field_name}' in value '{value}' is "
                            f"not of type '{args[0]}'."
                        )
                else:
                    raise ValidationError(
                        self.error_message
                        or f"Unsupported type '{field_type}' for field "
                        f"'{field_name}'."
                    )
            elif dataclasses.is_dataclass(field_type):
                IsDataclassValidator(field_type).validate(field_value)
            else:
                if not isinstance(field_value, field_type):
                    raise ValidationError(
                        self.error_message
                        or f"Field '{field_name}' in value '{value}' is not "
                        f"of type '{field_type}'."
                    )

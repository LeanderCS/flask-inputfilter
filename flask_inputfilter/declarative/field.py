from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

from flask_inputfilter.declarative import FieldDescriptor

if TYPE_CHECKING:
    from flask_inputfilter.models import (
        BaseFilter,
        BaseValidator,
        ExternalApiConfig,
    )


def field(
    *,
    required: bool = False,
    default: Any = None,
    fallback: Any = None,
    filters: Optional[list[BaseFilter]] = None,
    validators: Optional[list[BaseValidator]] = None,
    steps: Optional[list[Union[BaseFilter, BaseValidator]]] = None,
    external_api: Optional[ExternalApiConfig] = None,
    copy: Optional[str] = None,
    computed: Optional[Any] = None,
    input_filter: Optional[type] = None,
) -> FieldDescriptor:
    """
    Create a field descriptor for declarative field definition.

    This function creates a FieldDescriptor that can be used as a class
    attribute to define input filter fields declaratively.

    **Parameters:**

    - **required** (*bool*): Whether the field is required. Default: False.
    - **default** (*Any*): The default value of the field. Default: None.
    - **fallback** (*Any*): The fallback value of the field, if
      validations fail or field is None, although it is required.
      Default: None.
    - **filters** (*Optional[list[BaseFilter]]*): The filters to apply to
      the field value. Default: None.
    - **validators** (*Optional[list[BaseValidator]]*): The validators to
      apply to the field value. Default: None.
    - **steps** (*Optional[list[Union[BaseFilter, BaseValidator]]]*): Allows
      to apply multiple filters and validators in a specific order.
      Default: None.
    - **external_api** (*Optional[ExternalApiConfig]*): Configuration for an
      external API call. Default: None.
    - **copy** (*Optional[str]*): The name of the field to copy the value
      from. Default: None.
    - **computed** (*Optional[Callable[[dict[str, Any]], Any]]*): A callable
      that computes the field value from validated data.
      Default: None.
    - **input_filter** (*Optional[type]*): An InputFilter class to use
      for nested validation. When specified, the field value (must be a dict)
      will be validated against the nested InputFilter's rules. Default: None.

    **Returns:**

    A field descriptor configured with the given parameters.

    **Example:**

    .. code-block:: python

        from flask_inputfilter import InputFilter
        from flask_inputfilter.declarative import field
        from flask_inputfilter.validators import IsStringValidator

        class UserInputFilter(InputFilter):
            name: str = field(required=True, validators=[IsStringValidator()])
            age: int = field(required=True, default=18)
    """
    return FieldDescriptor(
        required=required,
        default=default,
        fallback=fallback,
        filters=filters,
        validators=validators,
        steps=steps,
        external_api=external_api,
        copy=copy,
        computed=computed,
        input_filter=input_filter,
    )

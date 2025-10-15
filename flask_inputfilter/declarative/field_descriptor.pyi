from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from flask_inputfilter.models import (
        BaseFilter,
        BaseValidator,
        ExternalApiConfig,
    )

class FieldDescriptor:
    """
    Descriptor class for declarative field definition using the field()
    decorator.

    This class stores all field configuration and is used by the metaclass
    to automatically register fields during class creation.

    **Parameters:**

    - **required** (*bool*): Whether the field is required.
    - **default** (*Any*): Default value if field is missing.
    - **fallback** (*Any*): Fallback value if validation fails.
    - **filters** (*Optional[list[BaseFilter]]*): List of filters to apply.
    - **validators** (*Optional[list[BaseValidator]]*): List of validators
      to apply.
    - **steps** (*Optional[list[Union[BaseFilter, BaseValidator]]]*): List of
      combined filters and validators.
    - **external_api** (*Optional[ExternalApiConfig]*): External API
      configuration.
    - **copy** (*Optional[str]*): Field to copy value from if this field
      is missing.
    - **computed** (*Optional[Callable[[dict[str, Any]], Any]]*): A
      callable that computes the field value from validated data.
    - **input_filter** (*Optional[type]*): An InputFilter class
      for nested validation.

    **Expected Behavior:**

    Automatically registers field configuration during class creation and
    provides
    attribute access to validated field values.
    """

    required: bool
    default: Any
    fallback: Any
    filters: list[BaseFilter]
    validators: list[BaseValidator]
    steps: list[Union[BaseFilter, BaseValidator]]
    external_api: Optional[ExternalApiConfig]
    copy: Optional[str]
    name: Optional[str]
    computed: Optional[Any]
    input_filter: Optional[type]

    def __init__(
        self,
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
    ) -> None: ...
    def __set_name__(self, owner: type, name: str) -> None: ...
    def __get__(self, obj: Any, objtype: Optional[type] = None) -> Any: ...
    def __set__(self, obj: Any, value: Any) -> None: ...
    def __repr__(self) -> str: ...

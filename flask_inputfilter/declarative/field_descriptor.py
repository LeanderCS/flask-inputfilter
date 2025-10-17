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
    - **computed** (*Optional[Callable[[dict[str, Any]], Any]]*): A callable
      that computes the field value from validated data.
    - **input_filter** (*Optional[type]*): An InputFilter class for
      nested validation.

    **Expected Behavior:**

    Automatically registers field configuration during class creation and
    provides
    attribute access to validated field values.
    """

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
    ) -> None:
        self.required = required
        self.default = default
        self.fallback = fallback
        self.filters = filters or []
        self.validators = validators or []
        self.steps = steps or []
        self.external_api = external_api
        self.copy = copy
        self.computed = computed
        self.input_filter = input_filter
        self.name: Optional[str] = None

    def __set_name__(self, owner: type, name: str) -> None:
        """
        Called when the descriptor is assigned to a class attribute.

        **Parameters:**

        - **owner** (*type*): The class that owns this descriptor.
        - **name** (*str*): The name of the attribute.
        """
        self.name = name

    def __get__(self, obj: Any, objtype: Optional[type] = None) -> Any:
        """
        Get the field value from the validated data.

        **Parameters:**

        - **obj** (*Any*): The InputFilter instance.
        - **objtype** (*Optional[type]*): The InputFilter class.

        **Returns:**

        The validated field value or None if not validated yet.
        """
        if obj is None:
            return self

        if hasattr(obj, "validated_data") and self.name:
            return obj.validated_data.get(self.name)

        return None

    def __set__(self, obj: Any, value: Any) -> None:
        """
        Set the field value in the raw data.

        **Parameters:**

        - **obj** (*Any*): The InputFilter instance.
        - **value** (*Any*): The value to set.
        """
        if self.name and hasattr(obj, "data"):
            obj.data[self.name] = value

    def __repr__(self) -> str:
        """String representation of the field descriptor."""
        return (
            f"FieldDescriptor("
            f"name={self.name!r}, "
            f"required={self.required}, "
            f"default={self.default!r}, "
            f"filters={len(self.filters)}, "
            f"validators={len(self.validators)}, "
            f"steps={len(self.steps)}, "
            f"external_api={self.external_api!r}, "
            f"copy={self.copy!r}, "
            f"computed={self.computed!r}, "
            f"input_filter={self.input_filter!r}"
            f")"
        )

# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, ExternalApiConfig

cdef class FieldDescriptor:
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

    def __cinit__(
        self,
        bint required = False,
        object default = None,
        object fallback = None,
        list[BaseFilter] filters = None,
        list[BaseValidator] validators = None,
        list[BaseFilter | BaseValidator] steps = None,
        ExternalApiConfig external_api = None,
        str copy = None,
        object computed = None,
        object input_filter = None,
    ) -> None:
        """
        Initialize a field descriptor.

        **Parameters:**

        - **required** (*bool*): Whether the field is required.
        - **default** (*Any*): The default value of the field.
        - **fallback** (*Any*): The fallback value of the field, if
          validations fail or field is None, although it is required.
        - **filters** (*Optional[list[BaseFilter]]*): The filters to apply to
          the field value.
        - **validators** (*Optional[list[BaseValidator]]*): The validators to
          apply to the field value.
        - **steps** (*Optional[list[Union[BaseFilter, BaseValidator]]]*): Allows
          to apply multiple filters and validators in a specific order.
        - **external_api** (*Optional[ExternalApiConfig]*): Configuration for an
          external API call.
        - **copy** (*Optional[str]*): The name of the field to copy the value
          from.
        - **computed** (*Optional[Callable[[dict[str, Any]], Any]]*): A callable
          that computes the field value from validated data.
        - **input_filter** (*Optional[type]*): An InputFilter class
          for nested validation.
        """
        self.required = required
        self._default = default
        self.fallback = fallback
        self.filters = filters if filters is not None else []
        self.validators = validators if validators is not None else []
        self.steps = steps if steps is not None else []
        self.external_api = external_api
        self.copy = copy
        self.computed = computed
        self.input_filter = input_filter
        self.name = None

    @property
    def default(self):
        """Get the default value."""
        return self._default

    @default.setter
    def default(self, value):
        """Set the default value."""
        self._default = value

    cpdef void __set_name__(self, object owner, str name):
        """
        Called when the descriptor is assigned to a class attribute.

        **Parameters:**

        - **owner** (*type*): The class that owns this descriptor.
        - **name** (*str*): The name of the attribute.
        """
        self.name = name

    def __get__(self, object obj, object objtype) -> object:
        """
        Get the field value from the validated data.

        **Parameters:**

        - **obj** (*Any*): The InputFilter instance.
        - **objtype** (*Optional[type]*): The InputFilter class.

        **Returns:**

        The validated field value or None if not validated yet.
        """
        cdef dict validated_data
        cdef object field_value

        if obj is None:
            return self

        if self.name is not None:
            validated_data = getattr(obj, "validated_data", None)
            if validated_data is not None:
                field_value = validated_data.get(self.name)
                if field_value is not None:
                    return field_value

        return None

    def __set__(self, object obj, object value) -> None:
        """
        Set the field value in the raw data.

        **Parameters:**

        - **obj** (*Any*): The InputFilter instance.
        - **value** (*Any*): The value to set.
        """
        cdef dict data

        if self.name is not None:
            data = getattr(obj, "data", None)
            if data is not None:
                data[self.name] = value

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

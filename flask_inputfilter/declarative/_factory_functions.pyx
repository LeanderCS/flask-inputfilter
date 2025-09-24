# cython: language_level=3

from ._field_descriptor cimport FieldDescriptor
from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, ExternalApiConfig

cpdef FieldDescriptor field(
    bint required = False,
    object default = None,
    object fallback = None,
    list[BaseFilter] filters = None,
    list[BaseValidator] validators = None,
    list steps = None,
    ExternalApiConfig external_api = None,
    str copy = None,
):
    """
    Create a field descriptor for declarative field definition.

    This function creates a FieldDescriptor that can be used as a class
    attribute to define input filter fields declaratively.

    **Parameters:**

    - **required** (*bool*): Whether the field is required. Default: False.
    - **default** (*Any*): The default value of the field. Default: None.
    - **fallback** (*Any*): The fallback value of the field, if
      validations fail or field is None, although it is required. Default: None.
    - **filters** (*Optional[list[BaseFilter]]*): The filters to apply to
      the field value. Default: None.
    - **validators** (*Optional[list[BaseValidator]]*): The validators to
      apply to the field value. Default: None.
    - **steps** (*Optional[list[Union[BaseFilter, BaseValidator]]]*): Allows
      to apply multiple filters and validators in a specific order. Default: None.
    - **external_api** (*Optional[ExternalApiConfig]*): Configuration for an
      external API call. Default: None.
    - **copy** (*Optional[str]*): The name of the field to copy the value
      from. Default: None.

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
    )

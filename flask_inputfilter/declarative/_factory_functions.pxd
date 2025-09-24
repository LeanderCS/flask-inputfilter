# cython: language_level=3

from flask_inputfilter.models.cimports cimport BaseFilter, BaseValidator, ExternalApiConfig
from ._field_descriptor cimport FieldDescriptor

cpdef FieldDescriptor field(
    bint required=*,
    object default=*,
    object fallback=*,
    list[BaseFilter] filters=*,
    list[BaseValidator] validators=*,
    list steps=*,
    ExternalApiConfig external_api=*,
    str copy=*
)
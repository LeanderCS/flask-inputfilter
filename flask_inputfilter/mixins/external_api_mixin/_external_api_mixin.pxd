from typing import Any

from flask_inputfilter.models.cimports cimport ExternalApiConfig


cdef class ExternalApiMixin:
    @staticmethod
    cdef str replace_placeholders(
        str value,
        dict[str, Any] validated_data
    )

    @staticmethod
    cdef dict[str, Any] replace_placeholders_in_params(
        dict[str, Any] params, dict[str, Any] validated_data
    )

    @staticmethod
    cdef object call_external_api(
        ExternalApiConfig config,
        object fallback,
        dict[str, Any] validated_data
    )

from typing import Any

from flask_inputfilter.models import ExternalApiConfig


cdef class ExternalApiMixin:
    @staticmethod
    cdef str replace_placeholders(
            str value,
            dict validated_data
    )
    @staticmethod
    cdef dict replace_placeholders_in_params(
           dict params, dict validated_data
    )
    @staticmethod
    cdef object call_external_api(object config, object fallback, dict validated_data)

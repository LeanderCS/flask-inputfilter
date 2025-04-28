from typing import Any, Dict

from flask_inputfilter.models import ExternalApiConfig


cdef class ExternalApiMixin:
    @staticmethod
    cdef str replace_placeholders(
            value: str,
            validated_data: Dict[str, Any]
    )
    @staticmethod
    cdef dict replace_placeholders_in_params(
            params: dict, validated_data: Dict[str, Any]
    )
    @staticmethod
    cdef object call_external_api(config: ExternalApiConfig, fallback: Any, validated_data: Dict[str, Any])

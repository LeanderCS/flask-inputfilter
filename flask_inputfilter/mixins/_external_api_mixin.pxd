from typing import Any, Dict

from flask_inputfilter.models import ExternalApiConfig


cdef class ExternalApiMixin:
    @staticmethod
    cdef str replacePlaceholders(
            value: str,
            validated_data: Dict[str, Any]
    )
    @staticmethod
    cdef dict replacePlaceholdersInParams(
            params: dict, validated_data: Dict[str, Any]
    )
    @staticmethod
    cdef object callExternalApi(config: ExternalApiConfig, fallback: Any, validated_data: Dict[str, Any])

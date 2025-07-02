try:
    from .data_mixin._data_mixin import DataMixin
    from .external_api_mixin._external_api_mixin import ExternalApiMixin
    from .validation_mixin._validation_mixin import ValidationMixin
except ImportError:
    from .data_mixin.data_mixin import DataMixin
    from .external_api_mixin.external_api_mixin import ExternalApiMixin
    from .validation_mixin.validation_mixin import ValidationMixin

__all__ = [
    "DataMixin",
    "ExternalApiMixin",
    "ValidationMixin",
]

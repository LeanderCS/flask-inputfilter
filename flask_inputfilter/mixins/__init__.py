import shutil

if shutil.which("g++") is not None:
    from .data_mixin._data_mixin import DataMixin
    from .external_api_mixin._external_api_mixin import ExternalApiMixin
    from .validation_mixin._validation_mixin import ValidationMixin

else:
    from .data_mixin.data_mixin import DataMixin
    from .external_api_mixin.external_api_mixin import ExternalApiMixin
    from .validation_mixin.validation_mixin import ValidationMixin

__all__ = [
    "DataMixin",
    "ExternalApiMixin",
    "ValidationMixin",
]

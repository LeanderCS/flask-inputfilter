import shutil

if shutil.which("g++") is not None:
    from .external_api_mixin._external_api_mixin import ExternalApiMixin
    from .field_mixin._field_mixin import FieldMixin

else:
    from .external_api_mixin.external_api_mixin import ExternalApiMixin
    from .field_mixin.field_mixin import FieldMixin

__all__ = [
    "ExternalApiMixin",
    "FieldMixin",
]

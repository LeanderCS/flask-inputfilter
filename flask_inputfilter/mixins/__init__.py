import shutil

if shutil.which("g++") is not None:
    from ._external_api_mixin import ExternalApiMixin
    from ._field_mixin import FieldMixin

else:
    from .external_api_mixin import ExternalApiMixin
    from .field_mixin import FieldMixin

__all__ = [
    "ExternalApiMixin",
    "FieldMixin",
]

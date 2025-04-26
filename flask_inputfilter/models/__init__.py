import shutil

from .external_api_config import ExternalApiConfig

if shutil.which("g++") is not None:
    from ._field_model import FieldModel

else:
    from .field_model import FieldModel

__all__ = [
    "FieldModel",
    "ExternalApiConfig",
]

import shutil

if shutil.which("g++") is not None:
    from ._base_filter import BaseFilter
    from ._external_api_config import ExternalApiConfig
    from ._field_model import FieldModel

else:
    from .base_filter import BaseFilter
    from .external_api_config import ExternalApiConfig
    from .field_model import FieldModel

__all__ = [
    "BaseFilter",
    "ExternalApiConfig",
    "FieldModel",
]

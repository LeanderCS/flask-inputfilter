import shutil

from .ExternalApiConfig import ExternalApiConfig

if shutil.which("g++") is not None:
    from ._FieldModel import FieldModel

else:
    from .FieldModel import FieldModel

import shutil

if shutil.which("g++") is not None:
    from ._ExternalApiMixin import ExternalApiMixin

else:
    from .ExternalApiMixin import ExternalApiMixin
    from .FieldMixin import FieldMixin

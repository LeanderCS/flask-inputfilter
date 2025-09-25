try:
    from ._factory_functions import field
    from ._field_descriptor import FieldDescriptor
except ImportError:
    from .factory_functions import field
    from .field_descriptor import FieldDescriptor

__all__ = [
    "FieldDescriptor",
    "field",
]

from __future__ import annotations

import inspect
from typing import Any


def register_class_attribute(attribute_name: str, value: Any) -> None:
    """
    Register an attribute on the calling class during class definition.

    This utility function uses frame inspection to access the class being
    defined and set an attribute on it. This is used by the declarative
    factory functions to register components during class definition.

    Args:
        attribute_name: The name of the attribute to set on the class
        value: The value to set for the attribute
    """
    try:
        frame = inspect.currentframe()
        if frame and frame.f_back and frame.f_back.f_back:
            caller_locals = frame.f_back.f_back.f_locals
            if (
                "__module__" in caller_locals
                and "__qualname__" in caller_locals
            ):
                caller_locals[attribute_name] = value
    except (AttributeError, KeyError):
        pass


def append_to_class_list(list_name: str, value: Any) -> None:
    """
    Append a value to a list attribute on the calling class during class
    definition.

    This utility function uses frame inspection to access the class being
    defined and append a value to a list attribute. If the list doesn't exist,
    it creates it first.

    Args:
        list_name: The name of the list attribute on the class
        value: The value to append to the list
    """
    try:
        frame = inspect.currentframe()
        if frame and frame.f_back and frame.f_back.f_back:
            caller_locals = frame.f_back.f_back.f_locals
            if (
                "__module__" in caller_locals
                and "__qualname__" in caller_locals
            ):
                if list_name not in caller_locals:
                    caller_locals[list_name] = []
                caller_locals[list_name].append(value)
    except (AttributeError, KeyError):
        pass

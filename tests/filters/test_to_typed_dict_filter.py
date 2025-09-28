import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToTypedDictFilter

try:
    from typing import TypedDict
    TYPEDDICT_AVAILABLE = True
except ImportError:
    try:
        from typing_extensions import TypedDict
        TYPEDDICT_AVAILABLE = True
    except ImportError:
        TYPEDDICT_AVAILABLE = False


class TestToTypedDictFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_dict_to_typed_dict(self) -> None:
        if TYPEDDICT_AVAILABLE:
            class Person(TypedDict):
                name: str
                age: int
        else:
            # Fallback for when TypedDict is not available
            class Person:
                __annotations__ = {"name": str, "age": int}

                def __init__(self, name: str, age: int) -> None:
                    self.name = name
                    self.age = age

                def __eq__(self, other):
                    if isinstance(other, dict):
                        return other == {"name": self.name, "age": self.age}
                    return NotImplemented

        self.input_filter.add(
            "person", required=True, filters=[ToTypedDictFilter(Person)]
        )

        validated_data = self.input_filter.validate_data(
            {"person": {"name": "John", "age": 25}}
        )
        self.assertEqual(validated_data["person"], {"name": "John", "age": 25})

    def test_non_dict_input_remains_unchanged(self) -> None:
        if TYPEDDICT_AVAILABLE:
            class Person(TypedDict):
                name: str
                age: int
        else:
            # Fallback for when TypedDict is not available
            class Person:
                __annotations__ = {"name": str, "age": int}

                def __init__(self, name: str, age: int) -> None:
                    self.name = name
                    self.age = age

        self.input_filter.add(
            "person", required=True, filters=[ToTypedDictFilter(Person)]
        )

        validated_data = self.input_filter.validate_data({"person": 123})
        self.assertEqual(validated_data["person"], 123)

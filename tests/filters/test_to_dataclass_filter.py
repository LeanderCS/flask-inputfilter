import unittest
from dataclasses import dataclass

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToDataclassFilter


class TestToDataclassFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_dict_to_dataclass(self) -> None:
        @dataclass
        class Person:
            name: str
            age: int

        self.input_filter.add(
            "person",
            required=True,
            filters=[ToDataclassFilter(Person)],
        )
        validated_data = self.input_filter.validateData(
            {"person": {"name": "John", "age": 25}}
        )
        self.assertEqual(validated_data["person"], Person("John", 25))

    def test_non_dict_input_remains_unchanged(self) -> None:
        @dataclass
        class Person:
            name: str
            age: int

        self.input_filter.add(
            "person",
            required=True,
            filters=[ToDataclassFilter(Person)],
        )
        validated_data = self.input_filter.validateData({"person": 123})
        self.assertEqual(validated_data["person"], 123)

import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import (
    ArrayElementFilter,
    StringSlugifyFilter,
    ToIntegerFilter,
    ToUpperFilter,
)


class TestArrayElementFilter(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.input_filter = InputFilter()

    def test_valid_array_elements(self) -> None:
        self.input_filter.add(
            "items", filters=[ArrayElementFilter(ToIntegerFilter())]
        )
        validated_data = self.input_filter.validate_data(
            {"items": ["1", "2", "3"]}
        )
        self.assertEqual(validated_data["items"], [1, 2, 3])

    def test_invalid_non_array_input(self) -> None:
        self.input_filter.add(
            "items", filters=[ArrayElementFilter(ToIntegerFilter())]
        )
        validated_data = self.input_filter.validate_data(
            {"items": "not an array"}
        )
        self.assertEqual(validated_data["items"], "not an array")

    def test_filter_with_multiple_filters(self) -> None:
        self.input_filter.add(
            "items",
            filters=[
                ArrayElementFilter([StringSlugifyFilter(), ToUpperFilter()])
            ],
        )
        validated_data = self.input_filter.validate_data(
            {"items": ["test test", "example example"]}
        )
        self.assertEqual(
            validated_data["items"], ["TEST-TEST", "EXAMPLE-EXAMPLE"]
        )

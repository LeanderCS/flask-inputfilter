import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ArrayExplodeFilter


class TestArrayExplodeFilter(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up a new InputFilter instance before each test.
        """
        self.input_filter = InputFilter()

    def test_explode_comma_separated_string(self) -> None:
        """
        Should explode a comma-separated string into a list.
        """
        self.input_filter.add(
            "tags",
            required=False,
            filters=[ArrayExplodeFilter()],
        )
        validated_data = self.input_filter.validateData(
            {"tags": "tag1,tag2,tag3"}
        )
        self.assertEqual(validated_data["tags"], ["tag1", "tag2", "tag3"])

    def test_explode_custom_separator_string(self) -> None:
        """
        Should explode a custom-separated string into a list.
        """
        self.input_filter.add(
            "items",
            required=False,
            filters=[ArrayExplodeFilter(";")],
        )
        validated_data = self.input_filter.validateData(
            {"items": "item1;item2;item3"}
        )
        self.assertEqual(validated_data["items"], ["item1", "item2", "item3"])

    def test_non_string_input_remains_unchanged(self) -> None:
        """
        Should return non-string input unchanged.
        """
        self.input_filter.add(
            "items",
            required=False,
            filters=[ArrayExplodeFilter(";")],
        )
        validated_data = self.input_filter.validateData({"items": 123})
        self.assertEqual(validated_data["items"], 123)

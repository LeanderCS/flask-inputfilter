import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToCamelCaseFilter


class TestToCamelCaseFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_string_to_camel_case(self) -> None:
        self.input_filter.add(
            "username",
            required=True,
            filters=[ToCamelCaseFilter()],
        )
        validated_data = self.input_filter.validate_data(
            {"username": "test user"}
        )
        self.assertEqual(validated_data["username"], "testUser")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "username",
            required=True,
            filters=[ToCamelCaseFilter()],
        )
        validated_data = self.input_filter.validate_data({"username": 123})
        self.assertEqual(validated_data["username"], 123)

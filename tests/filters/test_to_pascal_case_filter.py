import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToPascalCaseFilter


class TestToPascalCaseFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_to_pascal_case(self) -> None:
        self.input_filter.add(
            "username", required=True, filters=[ToPascalCaseFilter()]
        )

        validated_data = self.input_filter.validateData(
            {"username": "test user"}
        )
        self.assertEqual(validated_data["username"], "TestUser")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "username", required=True, filters=[ToPascalCaseFilter()]
        )

        validated_data = self.input_filter.validateData({"username": 123})
        self.assertEqual(validated_data["username"], 123)

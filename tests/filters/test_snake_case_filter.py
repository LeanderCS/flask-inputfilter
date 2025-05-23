import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToSnakeCaseFilter


class TestToSnakeCaseFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_to_snake_case(self) -> None:
        self.input_filter.add(
            "username", required=True, filters=[ToSnakeCaseFilter()]
        )

        validated_data = self.input_filter.validate_data(
            {"username": "TestUser"}
        )
        self.assertEqual(validated_data["username"], "test_user")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "username", required=True, filters=[ToSnakeCaseFilter()]
        )

        validated_data = self.input_filter.validate_data({"username": 123})
        self.assertEqual(validated_data["username"], 123)

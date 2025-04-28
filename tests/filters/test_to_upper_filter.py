import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToUpperFilter


class TestToUpperFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_to_uppercase(self) -> None:
        self.input_filter.add(
            "username", required=True, filters=[ToUpperFilter()]
        )

        validated_data = self.input_filter.validate_data(
            {"username": "testuser"}
        )
        self.assertEqual(validated_data["username"], "TESTUSER")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "username", required=True, filters=[ToUpperFilter()]
        )

        validated_data = self.input_filter.validate_data({"username": 123})
        self.assertEqual(validated_data["username"], 123)

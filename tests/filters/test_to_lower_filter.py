import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToLowerFilter


class TestToLowerFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_string_to_lowercase(self) -> None:
        self.input_filter.add(
            "username", required=True, filters=[ToLowerFilter()]
        )

        validated_data = self.input_filter.validateData(
            {"username": "TESTUSER"}
        )
        self.assertEqual(validated_data["username"], "testuser")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "username", required=True, filters=[ToLowerFilter()]
        )

        validated_data = self.input_filter.validateData({"username": 123})
        self.assertEqual(validated_data["username"], 123)

import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import TruncateFilter


class TestTruncateFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_truncates_string(self) -> None:
        self.input_filter.add(
            "truncated_field", required=False, filters=[TruncateFilter(5)]
        )

        validated_data = self.input_filter.validateData(
            {"truncated_field": "Hello World"}
        )
        self.assertEqual(validated_data["truncated_field"], "Hello")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "truncated_field", required=False, filters=[TruncateFilter(5)]
        )

        validated_data = self.input_filter.validateData(
            {"truncated_field": 123}
        )
        self.assertEqual(validated_data["truncated_field"], 123)

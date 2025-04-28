import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToNormalizedUnicodeFilter


class TestToNormalizedUnicodeFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_normalizes_unicode_characters(self) -> None:
        self.input_filter.add(
            "unicode_field",
            required=False,
            filters=[ToNormalizedUnicodeFilter()],
        )

        validated_data = self.input_filter.validate_data(
            {"unicode_field": "Héllô Wôrld"}
        )
        self.assertEqual(validated_data["unicode_field"], "Hello World")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "unicode_field",
            required=False,
            filters=[ToNormalizedUnicodeFilter()],
        )

        validated_data = self.input_filter.validate_data(
            {"unicode_field": 123}
        )
        self.assertEqual(validated_data["unicode_field"], 123)

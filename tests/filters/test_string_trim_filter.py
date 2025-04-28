import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import StringTrimFilter


class TestStringTrimFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_trims_whitespace(self) -> None:
        self.input_filter.add(
            "trimmed_field",
            required=False,
            filters=[StringTrimFilter()],
        )
        validated_data = self.input_filter.validate_data(
            {"trimmed_field": "   Hello World   "}
        )
        self.assertEqual(validated_data["trimmed_field"], "Hello World")

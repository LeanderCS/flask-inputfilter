import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import WhitespaceCollapseFilter


class TestWhitespaceCollapseFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_collapses_whitespace(self) -> None:
        self.input_filter.add(
            "collapsed_field",
            required=False,
            filters=[WhitespaceCollapseFilter()],
        )

        validated_data = self.input_filter.validate_data(
            {"collapsed_field": "Hello    World"}
        )
        self.assertEqual(validated_data["collapsed_field"], "Hello World")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "collapsed_field",
            required=False,
            filters=[WhitespaceCollapseFilter()],
        )

        validated_data = self.input_filter.validate_data(
            {"collapsed_field": 123}
        )
        self.assertEqual(validated_data["collapsed_field"], 123)

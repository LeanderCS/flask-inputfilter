import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToStringFilter


class TestToStringFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_to_string(self) -> None:
        self.input_filter.add("age", required=True, filters=[ToStringFilter()])

        validated_data = self.input_filter.validateData({"age": 25})
        self.assertEqual(validated_data["age"], "25")

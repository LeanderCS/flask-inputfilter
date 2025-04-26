import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToIntegerFilter


class TestToIntegerFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_to_integer(self) -> None:
        self.input_filter.add(
            "age", required=True, filters=[ToIntegerFilter()]
        )

        validated_data = self.input_filter.validateData({"age": "25"})
        self.assertEqual(validated_data["age"], 25)

        validated_data = self.input_filter.validateData({"age": 25.3})
        self.assertEqual(validated_data["age"], 25)

    def test_non_convertible_or_false_value_remains(self) -> None:
        self.input_filter.add(
            "age", required=True, filters=[ToIntegerFilter()]
        )

        validated_data = self.input_filter.validateData({"age": False})
        self.assertFalse(validated_data["age"])

        validated_data = self.input_filter.validateData({"age": "no integer"})
        self.assertEqual(validated_data["age"], "no integer")

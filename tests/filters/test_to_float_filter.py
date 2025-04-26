import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToFloatFilter


class TestToFloatFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_string_to_float(self) -> None:
        self.input_filter.add(
            "price", required=True, filters=[ToFloatFilter()]
        )

        validated_data = self.input_filter.validateData({"price": "19.99"})
        self.assertEqual(validated_data["price"], 19.99)

    def test_non_convertible_or_false_value_remains(self) -> None:
        self.input_filter.add(
            "price", required=True, filters=[ToFloatFilter()]
        )

        validated_data = self.input_filter.validateData({"price": False})
        self.assertFalse(validated_data["price"])

        validated_data = self.input_filter.validateData({"price": "no float"})
        self.assertEqual(validated_data["price"], "no float")

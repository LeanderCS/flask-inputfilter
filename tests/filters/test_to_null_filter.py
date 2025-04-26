import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToNullFilter


class TestToNullFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_transforms_empty_string_to_none(self) -> None:
        self.input_filter.add(
            "optional_field", required=False, filters=[ToNullFilter()]
        )

        validated_data = self.input_filter.validateData({"optional_field": ""})
        self.assertIsNone(validated_data["optional_field"])

import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToBooleanFilter


class TestToBooleanFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_string_to_boolean(self) -> None:
        self.input_filter.add(
            "is_active",
            required=True,
            filters=[ToBooleanFilter()],
        )
        validated_data = self.input_filter.validate_data({"is_active": "true"})
        self.assertTrue(validated_data["is_active"])

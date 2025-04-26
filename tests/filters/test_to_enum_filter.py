import unittest
from enum import Enum

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToEnumFilter


class TestToEnumFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_string_against_enum(self) -> None:
        class ColorEnum(Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

        self.input_filter.add(
            "color",
            required=True,
            filters=[ToEnumFilter(ColorEnum)],
        )

        validated_data = self.input_filter.validateData({"color": "red"})
        self.assertEqual(validated_data["color"], ColorEnum.RED)

        validated_data = self.input_filter.validateData({"color": "yellow"})
        self.assertEqual(validated_data["color"], "yellow")

        validated_data = self.input_filter.validateData({"color": 123})
        self.assertEqual(validated_data["color"], 123)

        validated_data = self.input_filter.validateData(
            {"color": ColorEnum.RED}
        )
        self.assertEqual(validated_data["color"], ColorEnum.RED)

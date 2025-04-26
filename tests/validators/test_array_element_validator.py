import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import ToIntegerFilter
from flask_inputfilter.validators import (
    ArrayElementValidator,
    IsIntegerValidator,
)


class TestArrayElementValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()
        self.element_filter = InputFilter()
        self.element_filter.add(
            "id",
            filters=[ToIntegerFilter()],
            validators=[IsIntegerValidator()],
        )

    def test_valid_array_elements(self) -> None:
        self.input_filter.add(
            "items", validators=[ArrayElementValidator(self.element_filter)]
        )
        validated_data = self.input_filter.validateData(
            {"items": [{"id": 1}, {"id": 2}]}
        )
        self.assertEqual(validated_data["items"], [{"id": 1}, {"id": 2}])

    def test_invalid_array_element(self) -> None:
        self.input_filter.add(
            "items", validators=[ArrayElementValidator(self.element_filter)]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"items": [{"id": 1}, {"id": "invalid"}]}
            )

    def test_invalid_non_array_input(self) -> None:
        self.input_filter.add(
            "items", validators=[ArrayElementValidator(self.element_filter)]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"items": "not an array"})

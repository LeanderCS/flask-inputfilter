import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import CustomJsonValidator


class TestCustomJsonValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_json_structure(self) -> None:
        self.input_filter.add(
            "data",
            validators=[
                CustomJsonValidator(
                    required_fields=["name", "age"], schema={"age": int}
                )
            ],
        )
        self.input_filter.validateData(
            {"data": '{"name": "Alice", "age": 25}'}
        )

    def test_invalid_missing_required_field(self) -> None:
        self.input_filter.add(
            "data",
            validators=[
                CustomJsonValidator(
                    required_fields=["name", "age"], schema={"age": int}
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"data": '{"name": "Alice"}'})

    def test_invalid_wrong_type(self) -> None:
        self.input_filter.add(
            "data",
            validators=[
                CustomJsonValidator(
                    required_fields=["name", "age"], schema={"age": int}
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"data": '{"name": "Alice", "age": "25"}'}
            )

    def test_invalid_not_json(self) -> None:
        self.input_filter.add(
            "data",
            validators=[
                CustomJsonValidator(
                    required_fields=["name", "age"], schema={"age": int}
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"data": "not a json"})

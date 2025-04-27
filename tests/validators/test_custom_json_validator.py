from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import CustomJsonValidator
from tests.validators import BaseValidatorTest


class TestCustomJsonValidator(BaseValidatorTest):
    def setUp(self) -> None:
        super().setUp()

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

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "data",
            validators=[
                CustomJsonValidator(
                    required_fields=["age"],
                    schema={"age": int},
                    error_message="Custom error message",
                )
            ],
        )
        self.assertValidationError(
            "data", {"age": "invalid"}, "Custom error message"
        )

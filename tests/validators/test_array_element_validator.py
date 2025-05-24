from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import ToIntegerFilter
from flask_inputfilter.validators import (
    ArrayElementValidator,
    IsIntegerValidator, IsStringValidator, LengthValidator,
)
from tests.validators import BaseValidatorTest


class TestArrayElementValidator(BaseValidatorTest):
    def setUp(self) -> None:
        super().setUp()
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
        validated_data = self.input_filter.validate_data(
            {"items": [{"id": 1}, {"id": 2}]}
        )
        self.assertEqual(validated_data["items"], [{"id": 1}, {"id": 2}])

    def test_invalid_array_element(self) -> None:
        self.input_filter.add(
            "items", validators=[ArrayElementValidator(self.element_filter)]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"items": [{"id": 1}, {"id": "invalid"}]}
            )

    def test_invalid_non_array_input(self) -> None:
        self.input_filter.add(
            "items", validators=[ArrayElementValidator(self.element_filter)]
        )
        self.assertValidationError(
            "items", "not an array", "Value 'not an array' is not an array"
        )

    def test_validator_with_direct_validator(self) -> None:
        self.input_filter.add(
            "items",
            validators=[
                ArrayElementValidator(
                    IsStringValidator()
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"items": ["str1", 123]})

        self.input_filter.validate_data({"items": ["str1", "str2"]})

    def test_validator_with_direct_validators(self) -> None:
        self.input_filter.add(
            "items",
            validators=[
                ArrayElementValidator([
                    IsStringValidator(),
                    LengthValidator(min_length=3, max_length=5)
                ])
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"items": ["str1", 123]})
            self.input_filter.validate_data({"items": ["str1", "stringtoolong"]})

        self.input_filter.validate_data({"items": ["str1", "str2"]})


    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "items",
            validators=[
                ArrayElementValidator(
                    self.element_filter, error_message="Custom error message"
                )
            ],
        )
        self.assertValidationError(
            "items", ["not an array"], "Custom error message"
        )

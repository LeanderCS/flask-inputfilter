from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsBase64ImageCorrectSizeValidator
from tests.validators import BaseValidatorTest


class TestIsBase64ImageCorrectSizeValidator(BaseValidatorTest):
    def test_valid_base64_size(self) -> None:
        self.input_filter.add(
            "image",
            validators=[
                IsBase64ImageCorrectSizeValidator(minSize=10, maxSize=50)
            ],
        )
        self.input_filter.validateData(
            {"image": "iVBORw0KGgoAAAANSUhEUgAAAAUA"}
        )

    def test_invalid_base64_size(self) -> None:
        self.input_filter.add(
            "image",
            validators=[
                IsBase64ImageCorrectSizeValidator(minSize=10, maxSize=50)
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"image": "short"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "image2",
            validators=[
                IsBase64ImageCorrectSizeValidator(
                    minSize=10, maxSize=5, error_message="Custom error"
                )
            ],
        )
        self.assertValidationError("image2", "too_small", "Custom error")

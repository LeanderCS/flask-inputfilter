import base64
import io
import unittest

from PIL import Image

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsHorizontalImageValidator


class TestIsHorizontalImageValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def _create_base64_image(self, width, height) -> str:
        img = Image.new("RGB", (width, height), color="red")
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()

    def test_valid_horizontal_image(self) -> None:
        self.input_filter.add(
            "image", validators=[IsHorizontalImageValidator()]
        )
        img_data = self._create_base64_image(100, 50)
        self.input_filter.validateData({"image": img_data})

    def test_invalid_vertical_image(self) -> None:
        self.input_filter.add(
            "image", validators=[IsHorizontalImageValidator()]
        )
        img_data = self._create_base64_image(50, 100)
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"image": img_data})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "image2",
            validators=[
                IsHorizontalImageValidator(error_message="Custom error")
            ],
        )
        img_data = self._create_base64_image(50, 100)
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"image2": img_data})

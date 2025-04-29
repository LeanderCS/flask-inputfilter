import base64
import io
import unittest

from PIL import Image

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import Base64ImageDownscaleFilter


class TestBase64ImageDownscaleFilter(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a new InputFilter instance before each test."""
        self.input_filter = InputFilter()

    def test_downscale_base64_image_string(self) -> None:
        """Should downscale a base64-encoded image string."""
        self.input_filter.add(
            "image",
            filters=[Base64ImageDownscaleFilter(size=144)],
        )
        with open("tests/data/base64_image.txt", "r") as file:
            validated_data = self.input_filter.validate_data(
                {"image": file.read()}
            )
            size = Image.open(
                io.BytesIO(base64.b64decode(validated_data["image"]))
            ).size
            self.assertEqual(size, (12, 12))

    def test_downscale_image_object(self) -> None:
        """Should downscale a Pillow image object."""
        self.input_filter.add(
            "image",
            filters=[Base64ImageDownscaleFilter(size=144)],
        )
        with open("tests/data/base64_image.txt", "r") as file:
            validated_data = self.input_filter.validate_data(
                {
                    "image": Image.open(
                        io.BytesIO(base64.b64decode(file.read()))
                    )
                }
            )
            size = Image.open(
                io.BytesIO(base64.b64decode(validated_data["image"]))
            ).size
            self.assertEqual(size, (12, 12))

    def test_non_image_input_remains_unchanged(self) -> None:
        """Should return non-image input unchanged."""
        self.input_filter.add(
            "image",
            filters=[Base64ImageDownscaleFilter(size=144)],
        )
        validated_data = self.input_filter.validate_data({"image": 123})
        self.assertEqual(validated_data["image"], 123)

        validated_data = self.input_filter.validate_data({"image": "no image"})
        self.assertEqual(validated_data["image"], "no image")

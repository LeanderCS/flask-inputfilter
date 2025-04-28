import base64
import io
import unittest

from PIL import Image

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import Base64ImageResizeFilter


class TestBase64ImageResizeFilter(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a new InputFilter instance before each test."""
        self.input_filter = InputFilter()

    def test_resize_base64_image_string_to_max_size(self) -> None:
        """Should resize a base64-encoded image so that it fits
        within the max size."""
        self.input_filter.add(
            "image",
            filters=[Base64ImageResizeFilter(max_size=1024)],
        )
        with open("tests/data/base64_image.txt", "r") as file:
            validated_data = self.input_filter.validate_data(
                {"image": file.read()}
            )
            image = Image.open(
                io.BytesIO(base64.b64decode(validated_data["image"]))
            )

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            size = buffer.tell()
            self.assertLessEqual(size, 1024)

    def test_resize_image_object_to_max_size(self) -> None:
        """Should resize a Pillow image object so that it fits within
        the max size."""
        self.input_filter.add(
            "image",
            filters=[Base64ImageResizeFilter(max_size=1024)],
        )
        with open("tests/data/base64_image.txt", "r") as file:
            validated_data = self.input_filter.validate_data(
                {
                    "image": Image.open(
                        io.BytesIO(base64.b64decode(file.read()))
                    )
                }
            )
            image = Image.open(
                io.BytesIO(base64.b64decode(validated_data["image"]))
            )

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            size = buffer.tell()
            self.assertLessEqual(size, 1024)

    def test_non_image_input_remains_unchanged(self) -> None:
        """Should return non-image input unchanged."""
        self.input_filter.add(
            "image",
            filters=[Base64ImageResizeFilter(max_size=1024)],
        )
        validated_data = self.input_filter.validate_data({"image": 123})
        self.assertEqual(validated_data["image"], 123)

        validated_data = self.input_filter.validate_data({"image": "no image"})
        self.assertEqual(validated_data["image"], "no image")

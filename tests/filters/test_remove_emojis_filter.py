import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import StringRemoveEmojisFilter


class TestStringRemoveEmojisFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_removes_emojis_from_string(self) -> None:
        self.input_filter.add(
            "text",
            required=False,
            filters=[StringRemoveEmojisFilter()],
        )
        validated_data = self.input_filter.validate_data(
            {"text": "Hello World! 😊"}
        )
        self.assertEqual(validated_data["text"], "Hello World! ")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "text",
            required=False,
            filters=[StringRemoveEmojisFilter()],
        )
        validated_data = self.input_filter.validate_data({"text": 123})
        self.assertEqual(validated_data["text"], 123)

import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import StringSlugifyFilter


class TestStringSlugifyFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_slugifies_string(self) -> None:
        self.input_filter.add(
            "slug",
            required=False,
            filters=[StringSlugifyFilter()],
        )
        validated_data = self.input_filter.validate_data(
            {"slug": "Hello World!"}
        )
        self.assertEqual(validated_data["slug"], "hello-world")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "slug",
            required=False,
            filters=[StringSlugifyFilter()],
        )
        validated_data = self.input_filter.validate_data({"slug": 123})
        self.assertEqual(validated_data["slug"], 123)

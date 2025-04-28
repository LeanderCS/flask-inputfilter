import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import WhitelistFilter


class TestWhitelistFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_filters_out_values_not_in_whitelist(self) -> None:
        self.input_filter.add(
            "whitelisted_field",
            required=False,
            filters=[WhitelistFilter(["test", "user"])],
        )

        validated_data = self.input_filter.validate_data(
            {"whitelisted_field": "test user admin"}
        )
        self.assertEqual(validated_data["whitelisted_field"], "test user")

    def test_filters_out_values_not_in_whitelist_from_array(self) -> None:
        self.input_filter.add(
            "whitelisted_field",
            required=False,
            filters=[WhitelistFilter(["test", "user"])],
        )

        validated_data = self.input_filter.validate_data(
            {"whitelisted_field": ["test", "user", "admin"]}
        )
        self.assertEqual(validated_data["whitelisted_field"], ["test", "user"])

    def test_filters_out_values_not_in_whitelist_from_dict(self) -> None:
        self.input_filter.add(
            "whitelisted_field",
            required=False,
            filters=[WhitelistFilter(["test", "user"])],
        )

        validated_data = self.input_filter.validate_data(
            {"whitelisted_field": {"test": "user", "admin": "admin"}}
        )
        self.assertEqual(validated_data["whitelisted_field"], {"test": "user"})

    def test_non_string_array_dict_remains_unchanged(self) -> None:
        self.input_filter.add(
            "whitelisted_field",
            required=False,
            filters=[WhitelistFilter(["test", "user"])],
        )

        validated_data = self.input_filter.validate_data(
            {"whitelisted_field": 123}
        )
        self.assertEqual(validated_data["whitelisted_field"], 123)

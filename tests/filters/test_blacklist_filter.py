import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import BlacklistFilter


class TestBlacklistFilter(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up a new InputFilter instance before each test.
        """
        self.input_filter = InputFilter()

    def test_blacklists_string_values(self) -> None:
        """
        Should remove blacklisted words from a string.
        """
        self.input_filter.add(
            "blacklisted_field",
            required=False,
            filters=[BlacklistFilter(["test", "user"])],
        )
        validated_data = self.input_filter.validate_data(
            {"blacklisted_field": "test user"}
        )
        self.assertEqual(validated_data["blacklisted_field"], "")

    def test_blacklists_array_values(self) -> None:
        """
        Should remove blacklisted values from an array.
        """
        self.input_filter.add(
            "blacklisted_field",
            required=False,
            filters=[BlacklistFilter(["test", "user"])],
        )
        validated_data = self.input_filter.validate_data(
            {"blacklisted_field": ["test", "user", "admin"]}
        )
        self.assertEqual(validated_data["blacklisted_field"], ["admin"])

    def test_blacklists_dict_keys(self) -> None:
        """
        Should remove blacklisted keys from a dictionary.
        """
        self.input_filter.add(
            "blacklisted_field",
            required=False,
            filters=[BlacklistFilter(["test", "user"])],
        )
        validated_data = self.input_filter.validate_data(
            {"blacklisted_field": {"test": "user", "admin": "admin"}}
        )
        self.assertEqual(
            validated_data["blacklisted_field"], {"admin": "admin"}
        )

    def test_non_string_array_dict_remains_unchanged(self) -> None:
        """
        Should leave non-string, non-array, non-dict values unchanged.
        """
        self.input_filter.add(
            "blacklisted_field",
            required=False,
            filters=[BlacklistFilter(["test", "user"])],
        )
        validated_data = self.input_filter.validate_data(
            {"blacklisted_field": 123}
        )
        self.assertEqual(validated_data["blacklisted_field"], 123)

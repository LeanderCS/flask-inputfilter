import unittest

from src.flask_inputfilter.Filter import (
    ToIntegerFilter,
    ToNullFilter,
    StringTrimFilter,
    ToFloatFilter,
    ToLowerFilter,
    ToUpperFilter,
    ToStringFilter,
    ToBooleanFilter,
    ArrayExplodeFilter,
    ToSnakeCaseFilter,
    ToPascaleCaseFilter,
    WhitespaceCollapseFilter,
)
from src.flask_inputfilter.InputFilter import InputFilter


class TestInputFilter(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up a InputFilter instance for testing.
        """

        self.inputFilter = InputFilter()

    def test_array_explode_filter(self) -> None:
        """
        Test that ArrayExplodeFilter explodes a string to a list.
        """

        self.inputFilter.add(
            "tags",
            required=False,
            filters=[ArrayExplodeFilter()],
        )

        validated_data = self.inputFilter.validateData({"tags": "tag1,tag2,tag3"})

        self.assertEqual(validated_data["tags"], ["tag1", "tag2", "tag3"])

        self.inputFilter.add("items", required=False, filters=[ArrayExplodeFilter(";")])

        validated_data = self.inputFilter.validateData({"items": "item1;item2;item3"})

        self.assertEqual(validated_data["items"], ["item1", "item2", "item3"])

    def test_string_trim_filter(self) -> None:
        """
        Test that StringTrimFilter trims whitespace.
        """

        self.inputFilter.add(
            "trimmed_field", required=False, filters=[StringTrimFilter()]
        )

        validated_data = self.inputFilter.validateData(
            {"trimmed_field": "   Hello World   "}
        )

        self.assertEqual(validated_data["trimmed_field"], "Hello World")

    def test_to_bool_filter(self) -> None:
        """
        Test that ToBooleanFilter converts string to boolean.
        """

        self.inputFilter.add("is_active", required=True, filters=[ToBooleanFilter()])

        validated_data = self.inputFilter.validateData({"is_active": "true"})

        self.assertTrue(validated_data["is_active"])

    def test_to_float_filter(self) -> None:
        """
        Test that ToFloatFilter converts string to float.
        """

        self.inputFilter.add("price", required=True, filters=[ToFloatFilter()])

        validated_data = self.inputFilter.validateData({"price": "19.99"})

        self.assertEqual(validated_data["price"], 19.99)

    def test_to_integer_filter(self) -> None:
        """
        Test that ToIntegerFilter converts string to integer.
        """

        self.inputFilter.add("age", required=True, filters=[ToIntegerFilter()])

        validated_data = self.inputFilter.validateData({"age": "25"})

        self.assertEqual(validated_data["age"], 25)

    def test_to_lower_filter(self) -> None:
        """
        Test that ToLowerFilter converts string to lowercase.
        """

        self.inputFilter.add("username", required=True, filters=[ToLowerFilter()])

        validated_data = self.inputFilter.validateData({"username": "TESTUSER"})

        self.assertEqual(validated_data["username"], "testuser")

    def test_to_null_filter(self) -> None:
        """
        Test that ToNullFilter transforms empty string to None.
        """

        self.inputFilter.add("optional_field", required=False, filters=[ToNullFilter()])

        validated_data = self.inputFilter.validateData({"optional_field": ""})

        self.assertIsNone(validated_data["optional_field"])

    def test_to_pascal_case_filter(self) -> None:
        """
        Test that PascalCaseFilter converts string to pascal case.
        """

        self.inputFilter.add("username", required=True, filters=[ToPascaleCaseFilter()])

        validated_data = self.inputFilter.validateData({"username": "test user"})

        self.assertEqual(validated_data["username"], "TestUser")

    def test_snake_case_filter(self) -> None:
        """
        Test that SnakeCaseFilter converts string to snake case.
        """

        self.inputFilter.add("username", required=True, filters=[ToSnakeCaseFilter()])

        validated_data = self.inputFilter.validateData({"username": "TestUser"})

        self.assertEqual(validated_data["username"], "test_user")

    def test_to_string_filter(self) -> None:
        """
        Test that ToStringFilter converts any type to string.
        """

        self.inputFilter.add("age", required=True, filters=[ToStringFilter()])

        validated_data = self.inputFilter.validateData({"age": 25})

        self.assertEqual(validated_data["age"], "25")

    def test_to_upper_filter(self) -> None:
        """
        Test that ToUpperFilter converts string to uppercase.
        """

        self.inputFilter.add("username", required=True, filters=[ToUpperFilter()])

        validated_data = self.inputFilter.validateData({"username": "testuser"})

        self.assertEqual(validated_data["username"], "TESTUSER")

    def test_whitespace_collapse_filter(self) -> None:
        """
        Test that WhitespaceCollapseFilter collapses whitespace.
        """

        self.inputFilter.add(
            "collapsed_field", required=False, filters=[WhitespaceCollapseFilter()]
        )

        validated_data = self.inputFilter.validateData(
            {"collapsed_field": "Hello    World"}
        )

        self.assertEqual(validated_data["collapsed_field"], "Hello World")

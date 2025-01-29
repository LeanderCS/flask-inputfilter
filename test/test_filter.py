import base64
import io
import unittest
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum

from PIL import Image
from typing_extensions import TypedDict

from flask_inputfilter import InputFilter
from flask_inputfilter.Filter import (
    ArrayExplodeFilter,
    Base64ImageDownscaleFilter,
    Base64ImageResizeFilter,
    BaseFilter,
    BlacklistFilter,
    RemoveEmojisFilter,
    SlugifyFilter,
    StringTrimFilter,
    ToAlphaNumericFilter,
    ToBooleanFilter,
    ToCamelCaseFilter,
    ToDataclassFilter,
    ToDateFilter,
    ToDateTimeFilter,
    ToEnumFilter,
    ToFloatFilter,
    ToIntegerFilter,
    ToIsoFilter,
    ToLowerFilter,
    ToNormalizedUnicodeFilter,
    ToNullFilter,
    ToPascaleCaseFilter,
    ToSnakeCaseFilter,
    ToStringFilter,
    ToTypedDictFilter,
    ToUpperFilter,
    TruncateFilter,
    WhitelistFilter,
    WhitespaceCollapseFilter,
)


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

        validated_data = self.inputFilter.validateData(
            {"tags": "tag1,tag2,tag3"}
        )
        self.assertEqual(validated_data["tags"], ["tag1", "tag2", "tag3"])

        self.inputFilter.add(
            "items", required=False, filters=[ArrayExplodeFilter(";")]
        )

        validated_data = self.inputFilter.validateData(
            {"items": "item1;item2;item3"}
        )
        self.assertEqual(validated_data["items"], ["item1", "item2", "item3"])

        validated_data = self.inputFilter.validateData({"items": 123})
        self.assertEqual(validated_data["items"], 123)

    def test_base64_image_downscale_filter(self) -> None:
        """
        Test Base64ImageDownscaleFilter.
        """

        self.inputFilter.add(
            "image",
            filters=[Base64ImageDownscaleFilter(size=144)],
        )

        with open("test/data/base64_image.txt", "r") as file:
            validated_data = self.inputFilter.validateData(
                {"image": file.read()}
            )
            size = Image.open(
                io.BytesIO(base64.b64decode(validated_data["image"]))
            ).size
            self.assertEqual(size, (12, 12))

        with open("test/data/base64_image.txt", "r") as file:
            validated_data = self.inputFilter.validateData(
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

        validated_data = self.inputFilter.validateData({"image": 123})
        self.assertEqual(validated_data["image"], 123)

        validated_data = self.inputFilter.validateData({"image": "no image"})
        self.assertEqual(validated_data["image"], "no image")

    def test_base64_image_size_reduce_filter(self) -> None:
        """
        Test Base64ImageResizeFilter.
        """

        self.inputFilter.add(
            "image",
            filters=[Base64ImageResizeFilter(max_size=1024)],
        )

        with open("test/data/base64_image.txt", "r") as file:
            validated_data = self.inputFilter.validateData(
                {"image": file.read()}
            )
            image = Image.open(
                io.BytesIO(base64.b64decode(validated_data["image"]))
            )

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            size = buffer.tell()
            self.assertLessEqual(size, 1024)

        with open("test/data/base64_image.txt", "r") as file:
            validated_data = self.inputFilter.validateData(
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

        validated_data = self.inputFilter.validateData({"image": 123})
        self.assertEqual(validated_data["image"], 123)

        validated_data = self.inputFilter.validateData({"image": "no image"})
        self.assertEqual(validated_data["image"], "no image")

    def test_base_filter(self) -> None:
        """
        Test that BaseFilter raises TypeError when apply
        method is called.
        """
        with self.assertRaises(TypeError):
            BaseFilter().apply("test")

    def test_blacklist_filter(self) -> None:
        """
        Test that BlacklistFilter filters out values that are in the blacklist.
        """
        self.inputFilter.add(
            "blacklisted_field",
            required=False,
            filters=[BlacklistFilter(["test", "user"])],
        )

        validated_data = self.inputFilter.validateData(
            {"blacklisted_field": "test user"}
        )
        self.assertEqual(validated_data["blacklisted_field"], "")

        validated_data = self.inputFilter.validateData(
            {"blacklisted_field": ["test", "user", "admin"]}
        )
        self.assertEqual(validated_data["blacklisted_field"], ["admin"])

        validated_data = self.inputFilter.validateData(
            {"blacklisted_field": {"test": "user", "admin": "admin"}}
        )
        self.assertEqual(
            validated_data["blacklisted_field"], {"admin": "admin"}
        )

        validated_data = self.inputFilter.validateData(
            {"blacklisted_field": 123}
        )
        self.assertEqual(validated_data["blacklisted_field"], 123)

    def test_remove_emojis_filter(self) -> None:
        """
        Test that RemoveEmojisFilter removes emojis from a string.
        """
        self.inputFilter.add(
            "text",
            required=False,
            filters=[RemoveEmojisFilter()],
        )

        validated_data = self.inputFilter.validateData(
            {"text": "Hello World! 😊"}
        )
        self.assertEqual(validated_data["text"], "Hello World! ")

        validated_data = self.inputFilter.validateData({"text": 123})
        self.assertEqual(validated_data["text"], 123)

    def test_slugify_filter(self) -> None:
        """
        Test that SlugifyFilter slugifies a string.
        """
        self.inputFilter.add(
            "slug",
            required=False,
            filters=[SlugifyFilter()],
        )

        validated_data = self.inputFilter.validateData(
            {"slug": "Hello World!"}
        )
        self.assertEqual(validated_data["slug"], "hello-world")

        validated_data = self.inputFilter.validateData({"slug": 123})
        self.assertEqual(validated_data["slug"], 123)

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

    def test_to_alphanumeric_filter(self) -> None:
        """
        Test that ToAlphaNumericFilter removes non-alphanumeric characters.
        """
        self.inputFilter.add(
            "alphanumeric_field",
            required=False,
            filters=[ToAlphaNumericFilter()],
        )

        validated_data = self.inputFilter.validateData(
            {"alphanumeric_field": "Hello World!123"}
        )
        self.assertEqual(validated_data["alphanumeric_field"], "HelloWorld123")

        validated_data = self.inputFilter.validateData(
            {"alphanumeric_field": 123}
        )
        self.assertEqual(validated_data["alphanumeric_field"], 123)

    def test_to_boolean_filter(self) -> None:
        """
        Test that ToBooleanFilter converts string to boolean.
        """
        self.inputFilter.add(
            "is_active", required=True, filters=[ToBooleanFilter()]
        )

        validated_data = self.inputFilter.validateData({"is_active": "true"})
        self.assertTrue(validated_data["is_active"])

    def test_to_camel_case_filter(self) -> None:
        """
        Test that CamelCaseFilter converts string to camel case.
        """
        self.inputFilter.add(
            "username", required=True, filters=[ToCamelCaseFilter()]
        )

        validated_data = self.inputFilter.validateData(
            {"username": "test user"}
        )
        self.assertEqual(validated_data["username"], "testUser")

        validated_data = self.inputFilter.validateData({"username": 123})
        self.assertEqual(validated_data["username"], 123)

    def test_to_dataclass_filter(self) -> None:
        """
        Test that ToDataclassFilter converts a dictionary to a dataclass.
        """

        @dataclass
        class Person:
            name: str
            age: int

        self.inputFilter.add(
            "person", required=True, filters=[ToDataclassFilter(Person)]
        )

        validated_data = self.inputFilter.validateData(
            {"person": {"name": "John", "age": 25}}
        )
        self.assertEqual(validated_data["person"], Person("John", 25))

        validated_data = self.inputFilter.validateData({"person": 123})
        self.assertEqual(validated_data["person"], 123)

    def test_to_date_filter(self) -> None:
        """
        Test that ToDateFilter converts string to date.
        """
        self.inputFilter.add("dob", required=True, filters=[ToDateFilter()])

        validated_data = self.inputFilter.validateData({"dob": "1996-12-01"})
        self.assertEqual(validated_data["dob"], date(1996, 12, 1))

        validated_data = self.inputFilter.validateData(
            {"dob": date(1996, 12, 1)}
        )
        self.assertEqual(validated_data["dob"], date(1996, 12, 1))

        validated_data = self.inputFilter.validateData(
            {"dob": datetime(1996, 12, 1, 12, 0, 0)}
        )
        self.assertEqual(validated_data["dob"], date(1996, 12, 1))

        validated_data = self.inputFilter.validateData({"dob": "no date"})
        self.assertEqual(validated_data["dob"], "no date")

        validated_data = self.inputFilter.validateData({"dob": 123})
        self.assertEqual(validated_data["dob"], 123)

    def test_to_datetime_filter(self) -> None:
        """
        Test that ToDateTimeFilter converts string to datetime.
        """
        self.inputFilter.add(
            "created_at", required=True, filters=[ToDateTimeFilter()]
        )

        validated_data = self.inputFilter.validateData(
            {"created_at": "2021-01-01T12:00:00"}
        )
        self.assertEqual(
            validated_data["created_at"],
            datetime(2021, 1, 1, 12, 0, 0),
        )

        validated_data = self.inputFilter.validateData(
            {"created_at": date(2021, 1, 1)}
        )
        self.assertEqual(
            validated_data["created_at"],
            datetime(2021, 1, 1, 0, 0, 0),
        )

        validated_data = self.inputFilter.validateData(
            {"created_at": datetime(2021, 1, 1, 12, 0, 0)}
        )
        self.assertEqual(
            validated_data["created_at"],
            datetime(2021, 1, 1, 12, 0, 0),
        )

        validated_data = self.inputFilter.validateData(
            {"created_at": "no date"}
        )
        self.assertEqual(validated_data["created_at"], "no date")

        validated_data = self.inputFilter.validateData({"created_at": 123})
        self.assertEqual(validated_data["created_at"], 123)

    def test_to_enum_filter(self) -> None:
        """
        Test that EnumFilter validates a string against a list of values.
        """

        class ColorEnum(Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

        self.inputFilter.add(
            "color",
            required=True,
            filters=[ToEnumFilter(ColorEnum)],
        )

        validated_data = self.inputFilter.validateData({"color": "red"})
        self.assertEqual(validated_data["color"], ColorEnum.RED)

        validated_data = self.inputFilter.validateData({"color": "yellow"})
        self.assertEqual(validated_data["color"], "yellow")

        validated_data = self.inputFilter.validateData({"color": 123})
        self.assertEqual(validated_data["color"], 123)

        validated_data = self.inputFilter.validateData(
            {"color": ColorEnum.RED}
        )
        self.assertEqual(validated_data["color"], ColorEnum.RED)

    def test_to_float_filter(self) -> None:
        """
        Test that ToFloatFilter converts string to float.
        """
        self.inputFilter.add("price", required=True, filters=[ToFloatFilter()])

        validated_data = self.inputFilter.validateData({"price": "19.99"})
        self.assertEqual(validated_data["price"], 19.99)

        validated_data = self.inputFilter.validateData({"price": False})
        self.assertEqual(validated_data["price"], False)

        validated_data = self.inputFilter.validateData({"price": "no float"})
        self.assertEqual(validated_data["price"], "no float")

    def test_to_integer_filter(self) -> None:
        """
        Test that ToIntegerFilter converts string to integer.
        """
        self.inputFilter.add("age", required=True, filters=[ToIntegerFilter()])

        validated_data = self.inputFilter.validateData({"age": "25"})
        self.assertEqual(validated_data["age"], 25)

        validated_data = self.inputFilter.validateData({"age": 25.3})
        self.assertEqual(validated_data["age"], 25)

        validated_data = self.inputFilter.validateData({"age": False})
        self.assertEqual(validated_data["age"], False)

        validated_data = self.inputFilter.validateData({"age": "no integer"})
        self.assertEqual(validated_data["age"], "no integer")

    def test_to_iso_filter(self) -> None:
        """
        Test that ToIsoFilter converts date or datetime to
        ISO 8601 formatted string.
        """
        self.inputFilter.add("date", filters=[ToIsoFilter()])

        validated_data = self.inputFilter.validateData(
            {"date": date(2021, 1, 1)}
        )
        self.assertEqual(validated_data["date"], "2021-01-01")

        validated_data = self.inputFilter.validateData(
            {"date": datetime(2021, 1, 1, 12, 0, 0)}
        )
        self.assertEqual(validated_data["date"], "2021-01-01T12:00:00")

        validated_data = self.inputFilter.validateData(
            {"date": "2020-01-01T12:00:00"}
        )
        self.assertEqual(validated_data["date"], "2020-01-01T12:00:00")

        validated_data = self.inputFilter.validateData({"date": "no date"})
        self.assertEqual(validated_data["date"], "no date")

    def test_to_lower_filter(self) -> None:
        """
        Test that ToLowerFilter converts string to lowercase.
        """
        self.inputFilter.add(
            "username", required=True, filters=[ToLowerFilter()]
        )

        validated_data = self.inputFilter.validateData(
            {"username": "TESTUSER"}
        )
        self.assertEqual(validated_data["username"], "testuser")

        validated_data = self.inputFilter.validateData({"username": 123})
        self.assertEqual(validated_data["username"], 123)

    def test_to_normalized_unicode_filter(self) -> None:
        """
        Test that NormalizeUnicodeFilter normalizes Unicode characters.
        """
        self.inputFilter.add(
            "unicode_field",
            required=False,
            filters=[ToNormalizedUnicodeFilter()],
        )

        validated_data = self.inputFilter.validateData(
            {"unicode_field": "Héllô Wôrld"}
        )
        self.assertEqual(validated_data["unicode_field"], "Hello World")

        validated_data = self.inputFilter.validateData({"unicode_field": 123})
        self.assertEqual(validated_data["unicode_field"], 123)

    def test_to_null_filter(self) -> None:
        """
        Test that ToNullFilter transforms empty string to None.
        """
        self.inputFilter.add(
            "optional_field", required=False, filters=[ToNullFilter()]
        )

        validated_data = self.inputFilter.validateData({"optional_field": ""})
        self.assertIsNone(validated_data["optional_field"])

    def test_to_pascal_case_filter(self) -> None:
        """
        Test that PascalCaseFilter converts string to pascal case.
        """
        self.inputFilter.add(
            "username", required=True, filters=[ToPascaleCaseFilter()]
        )

        validated_data = self.inputFilter.validateData(
            {"username": "test user"}
        )
        self.assertEqual(validated_data["username"], "TestUser")

        validated_data = self.inputFilter.validateData({"username": 123})
        self.assertEqual(validated_data["username"], 123)

    def test_snake_case_filter(self) -> None:
        """
        Test that SnakeCaseFilter converts string to snake case.
        """
        self.inputFilter.add(
            "username", required=True, filters=[ToSnakeCaseFilter()]
        )

        validated_data = self.inputFilter.validateData(
            {"username": "TestUser"}
        )
        self.assertEqual(validated_data["username"], "test_user")

        validated_data = self.inputFilter.validateData({"username": 123})
        self.assertEqual(validated_data["username"], 123)

    def test_to_string_filter(self) -> None:
        """
        Test that ToStringFilter converts any type to string.
        """
        self.inputFilter.add("age", required=True, filters=[ToStringFilter()])

        validated_data = self.inputFilter.validateData({"age": 25})
        self.assertEqual(validated_data["age"], "25")

    def test_to_typed_dict_filter(self) -> None:
        """
        Test that ToTypedDictFilter converts a dictionary to a TypedDict.
        """

        class Person(TypedDict):
            name: str
            age: int

        self.inputFilter.add(
            "person", required=True, filters=[ToTypedDictFilter(Person)]
        )

        validated_data = self.inputFilter.validateData(
            {"person": {"name": "John", "age": 25}}
        )
        self.assertEqual(validated_data["person"], {"name": "John", "age": 25})

        validated_data = self.inputFilter.validateData({"person": 123})
        self.assertEqual(validated_data["person"], 123)

    def test_to_upper_filter(self) -> None:
        """
        Test that ToUpperFilter converts string to uppercase.
        """
        self.inputFilter.add(
            "username", required=True, filters=[ToUpperFilter()]
        )

        validated_data = self.inputFilter.validateData(
            {"username": "testuser"}
        )
        self.assertEqual(validated_data["username"], "TESTUSER")

        validated_data = self.inputFilter.validateData({"username": 123})
        self.assertEqual(validated_data["username"], 123)

    def test_truncate_filter(self) -> None:
        """
        Test that TruncateFilter truncates a string.
        """
        self.inputFilter.add(
            "truncated_field", required=False, filters=[TruncateFilter(5)]
        )

        validated_data = self.inputFilter.validateData(
            {"truncated_field": "Hello World"}
        )
        self.assertEqual(validated_data["truncated_field"], "Hello")

        validated_data = self.inputFilter.validateData(
            {"truncated_field": 123}
        )
        self.assertEqual(validated_data["truncated_field"], 123)

    def test_whitelist_filter(self) -> None:
        """
        Test that WhitelistFilter filters out values that are
        not in the whitelist.
        """
        self.inputFilter.add(
            "whitelisted_field",
            required=False,
            filters=[WhitelistFilter(["test", "user"])],
        )

        validated_data = self.inputFilter.validateData(
            {"whitelisted_field": "test user admin"}
        )
        self.assertEqual(validated_data["whitelisted_field"], "test user")

        validated_data = self.inputFilter.validateData(
            {"whitelisted_field": ["test", "user", "admin"]}
        )
        self.assertEqual(validated_data["whitelisted_field"], ["test", "user"])

        validated_data = self.inputFilter.validateData(
            {"whitelisted_field": {"test": "user", "admin": "admin"}}
        )
        self.assertEqual(validated_data["whitelisted_field"], {"test": "user"})

        validated_data = self.inputFilter.validateData(
            {"whitelisted_field": 123}
        )
        self.assertEqual(validated_data["whitelisted_field"], 123)

    def test_whitespace_collapse_filter(self) -> None:
        """
        Test that WhitespaceCollapseFilter collapses whitespace.
        """
        self.inputFilter.add(
            "collapsed_field",
            required=False,
            filters=[WhitespaceCollapseFilter()],
        )

        validated_data = self.inputFilter.validateData(
            {"collapsed_field": "Hello    World"}
        )
        self.assertEqual(validated_data["collapsed_field"], "Hello World")

        validated_data = self.inputFilter.validateData(
            {"collapsed_field": 123}
        )
        self.assertEqual(validated_data["collapsed_field"], 123)


if __name__ == "__main__":
    unittest.main()

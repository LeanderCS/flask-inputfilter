import unittest
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum

from typing_extensions import TypedDict

from flask_inputfilter import InputFilter
from flask_inputfilter.Enum import RegexEnum
from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Filter import Base64ImageDownscaleFilter
from flask_inputfilter.Validator import (
    ArrayElementValidator,
    ArrayLengthValidator,
    BaseValidator,
    CustomJsonValidator,
    DateAfterValidator,
    DateBeforeValidator,
    DateRangeValidator,
    FloatPrecisionValidator,
    InArrayValidator,
    InEnumValidator,
    IsArrayValidator,
    IsBase64ImageCorrectSizeValidator,
    IsBase64ImageValidator,
    IsBooleanValidator,
    IsDataclassValidator,
    IsFloatValidator,
    IsFutureDateValidator,
    IsHexadecimalValidator,
    IsHorizontalImageValidator,
    IsInstanceValidator,
    IsIntegerValidator,
    IsJsonValidator,
    IsPastDateValidator,
    IsStringValidator,
    IsTypedDictValidator,
    IsUUIDValidator,
    IsVerticalImageValidator,
    IsWeekdayValidator,
    IsWeekendValidator,
    LengthValidator,
    NotInArrayValidator,
    NotValidator,
    RangeValidator,
    RegexValidator,
)


class TestInputFilter(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up a InputFilter instance for testing.
        """

        self.inputFilter = InputFilter()

    def test_array_element_validator(self) -> None:
        """
        Test ArrayElementValidator.
        """

        elementFilter = InputFilter()
        elementFilter.add(
            "id",
            validators=[IsIntegerValidator()],
        )

        self.inputFilter.add(
            "items",
            validators=[ArrayElementValidator(elementFilter)],
        )

        validated_data = self.inputFilter.validateData(
            {"items": [{"id": 1}, {"id": 2}]}
        )
        self.assertEqual(validated_data["items"], [{"id": 1}, {"id": 2}])

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"items": [{"id": 1}, {"id": "invalid"}]}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"items": "not an array"})

        self.inputFilter.add(
            "items",
            validators=[
                ArrayElementValidator(elementFilter, "Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"items": [{"id": 1}, {"id": "invalid"}]}
            )

    def test_array_length_validator(self) -> None:
        """
        Test ArrayLengthValidator.
        """

        self.inputFilter.add(
            "items",
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )

        self.inputFilter.validateData({"items": [1, 2, 3, 4]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"items": [1]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"items": [1, 2, 3, 4, 5, 6]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"items": "not an array"})

        self.inputFilter.add(
            "items",
            validators=[
                ArrayLengthValidator(
                    max_length=10, error_message="custom error message"
                )
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"items": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}
            )

    def test_base_validator(self) -> None:
        """
        Test BaseValidator.
        """

        with self.assertRaises(TypeError):
            BaseValidator().validate("value")

    def test_custom_json_validator(self) -> None:
        """
        Test CustomJsonValidator.
        """

        self.inputFilter.add(
            "data",
            validators=[
                CustomJsonValidator(
                    required_fields=["name", "age"],
                    schema={"age": int},
                )
            ],
        )

        self.inputFilter.validateData({"data": '{"name": "Alice", "age": 25}'})
        self.inputFilter.validateData(
            {"data": '{"name": "Alice", "age": 25, "extra": "extra"}'}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data": '{"name": "Alice"}'})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"data": '{"name": "Alice", "age": "25"}'}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"data": '{"name": "Alice", "age": 25.5}'}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data": "not a json"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data": 123})

        self.inputFilter.add(
            "data",
            validators=[
                CustomJsonValidator(
                    required_fields=["name", "age"],
                    schema={"age": int},
                    error_message="Custom error message",
                )
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data": '{"name": "Alice"}'})

    def test_date_after_validator(self) -> None:
        """
        Test DateAfterValidator.
        """

        self.inputFilter.add(
            "date",
            validators=[DateAfterValidator(reference_date=date(2021, 1, 1))],
        )
        self.inputFilter.validateData({"date": date(2021, 6, 1)})
        self.inputFilter.validateData({"date": datetime(2021, 6, 1, 0, 0)})
        self.inputFilter.validateData({"date": "2021-06-02T10:00:55"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": date(2020, 12, 31)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"date": datetime(2020, 12, 31, 23, 59)}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": "2020-12-31T23:59:59"})

        self.inputFilter.add(
            "datetime",
            validators=[
                DateAfterValidator(
                    reference_date=datetime(2021, 1, 1, 0, 0),
                )
            ],
        )
        self.inputFilter.validateData(
            {"datetime": datetime(2021, 6, 1, 12, 0)}
        )
        self.inputFilter.validateData({"datetime": "2021-06-01T12:00:00"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"datetime": datetime(2020, 12, 31, 23, 59)}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"datetime": "2020-12-31T23:59:59"})

        self.inputFilter.add(
            "isodatetime",
            validators=[
                DateAfterValidator(
                    reference_date="2021-01-01T00:00:00",
                )
            ],
        )
        self.inputFilter.validateData({"isodatetime": "2021-06-01T00:00:00"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"isodatetime": "2020-12-31T23:59:59"}
            )

        self.inputFilter.add(
            "custom_error",
            validators=[
                DateAfterValidator(
                    reference_date="2021-01-01T00:00:00",
                    error_message="Custom error message",
                )
            ],
        )

        with self.assertRaises(ValidationError) as context:
            self.inputFilter.validateData(
                {"custom_error": "2020-12-31T23:59:59"}
            )
        self.assertEqual(str(context.exception), "Custom error message")

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_error": "unparseable date"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_error": 123})

    def test_date_before_validator(self) -> None:
        """
        Test DateBeforeValidator.
        """

        self.inputFilter.add(
            "date",
            validators=[
                DateBeforeValidator(reference_date=date(2021, 12, 31))
            ],
        )

        self.inputFilter.validateData({"date": date(2021, 6, 1)})
        self.inputFilter.validateData({"date": datetime(2021, 6, 1, 0, 0)})
        self.inputFilter.validateData({"date": "2021-06-01T10:00:55"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": date(2022, 6, 1)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"date": datetime(2022, 6, 1, 0, 54)}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": "20"})

        self.inputFilter.add(
            "datetime",
            validators=[
                DateBeforeValidator(
                    reference_date=datetime(2021, 12, 31, 0, 0),
                )
            ],
        )

        self.inputFilter.validateData({"datetime": date(2021, 6, 1)})
        self.inputFilter.validateData(
            {"datetime": datetime(2021, 6, 1, 12, 0)}
        )
        self.inputFilter.validateData({"datetime": "2021-06-01T00:00:00"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"datetime": date(2022, 6, 1)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"datetime": datetime(2022, 6, 1, 0, 0)}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"datetime": "2022-06-01T00:00:00"})

        self.inputFilter.add(
            "isodatetime",
            validators=[
                DateBeforeValidator(
                    reference_date="2021-12-31T00:00:00",
                )
            ],
        )

        self.inputFilter.validateData({"isodatetime": date(2021, 6, 1)})
        self.inputFilter.validateData(
            {"isodatetime": datetime(2021, 6, 1, 12, 0)}
        )
        self.inputFilter.validateData({"isodatetime": "2021-06-01T00:00:00"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"isodatetime": date(2022, 6, 1)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"isodatetime": datetime(2022, 6, 1, 10, 0)}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"isodatetime": "2022-06-01T00:00:00"}
            )

        self.inputFilter.add(
            "custom_error",
            validators=[
                DateBeforeValidator(
                    reference_date="2021-12-31T00:00:00",
                    error_message="Custom error message",
                )
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"custom_error": "2022-06-01T00:00:00"}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_error": "unparseable date"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_error": 123})

    def test_date_range_validator(self) -> None:
        """
        Test DateRangeValidator.
        """

        self.inputFilter.add(
            "date",
            validators=[DateRangeValidator(max_date=date(2021, 12, 31))],
        )

        self.inputFilter.validateData({"date": date(2021, 6, 1)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": date(2022, 6, 1)})

        self.inputFilter.add(
            "datetime",
            validators=[
                DateRangeValidator(
                    min_date=datetime(2021, 1, 1, 0, 0),
                )
            ],
        )

        self.inputFilter.validateData({"datetime": date(2021, 6, 1)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"datetime": date(2020, 6, 1)})

        self.inputFilter.add(
            "iso_date",
            validators=[
                DateRangeValidator(
                    min_date="2021-01-12T22:26:08.542945",
                    max_date="2021-01-24T22:26:08.542945",
                )
            ],
        )

        self.inputFilter.validateData(
            {"iso_date": "2021-01-15T22:26:08.542945"}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"iso_date": "2022-01-15T22:26:08.542945"}
            )

        self.inputFilter.add(
            "custom_error",
            validators=[
                DateRangeValidator(
                    max_date="2021-01-24T22:26:08.542945",
                    error_message="Custom error message",
                )
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"custom_error": "2022-12-31T23:59:59"}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_error": "unparseable date"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_error": 123})

    def test_float_precision_validator(self) -> None:
        """
        Test FloatPrecisionValidator.
        """

        self.inputFilter.add(
            "price",
            validators=[FloatPrecisionValidator(precision=5, scale=2)],
        )

        self.inputFilter.validateData({"price": 19.99})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"price": 19.999})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"price": 1999.99})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"price": "not a float"})

        self.inputFilter.add(
            "custom_message2",
            validators=[
                FloatPrecisionValidator(
                    precision=5, scale=2, error_message="Custom error message"
                )
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_message2": 19.999})

    def test_in_array_validator(self) -> None:
        """
        Test InArrayValidator.
        """

        self.inputFilter.add(
            "color",
            validators=[InArrayValidator(["red", "green", "blue"])],
        )

        self.inputFilter.validateData({"color": "red"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"color": "yellow"})

        self.inputFilter.add(
            "color_strict",
            validators=[InArrayValidator(["red", "green", "blue"], True)],
        )

        self.inputFilter.validateData({"color_strict": "red"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"color_strict": 1})

        self.inputFilter.add(
            "custom_error2",
            validators=[
                InArrayValidator(
                    ["red", "green", "blue"],
                    error_message="Custom error message",
                )
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_error2": "yellow"})

    def test_in_enum_validator(self) -> None:
        """
        Test InEnumValidator.
        """

        class Color(Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

        self.inputFilter.add("color", validators=[InEnumValidator(Color)])

        self.inputFilter.validateData({"color": "red"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"color": "yellow"})

        self.inputFilter.add(
            "custom_error2",
            validators=[
                InEnumValidator(Color, error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_error2": "yellow"})

    def test_is_array_validator(self) -> None:
        """
        Test that IsArrayValidator validates array type.
        """

        self.inputFilter.add("tags", validators=[IsArrayValidator()])

        self.inputFilter.validateData({"tags": ["tag1", "tag2"]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"tags": "not_an_array"})

        self.inputFilter.add(
            "tags2",
            validators=[
                IsArrayValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"tags2": "not_an_array"})

    def test_is_base64_image_correct_size_validator(self) -> None:
        """
        Test IsBase64ImageCorrectSizeValidator.
        """

        self.inputFilter.add(
            "image",
            validators=[
                IsBase64ImageCorrectSizeValidator(minSize=10, maxSize=50)
            ],
        )

        self.inputFilter.validateData(
            {"image": "iVBORw0KGgoAAAANSUhEUgAAAAUA"}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"image": "iVBORw0KGgoAAAANSUhEUgAAAAU"}
            )

        self.inputFilter.add(
            "image2",
            validators=[
                IsBase64ImageCorrectSizeValidator(
                    minSize=10,
                    maxSize=5,
                    error_message="Custom error message",
                )
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"image2": "iVBORw0KGgoAAAANSUhEUgAAAAU"}
            )

    def test_is_base64_image_validator(self) -> None:
        """
        Test IsBase64ImageValidator.
        """

        self.inputFilter.add(
            "image", required=True, validators=[IsBase64ImageValidator()]
        )

        with open("test/data/base64_image.txt", "r") as file:
            self.inputFilter.validateData({"image": file.read()})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"image": "not_a_base64_image"})

    def test_is_boolean_validator(self) -> None:
        """
        Test IsBooleanValidator.
        """

        self.inputFilter.add("is_active", validators=[IsBooleanValidator()])

        self.inputFilter.validateData({"is_active": True})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"is_active": "yes"})

        self.inputFilter.add(
            "is_active2",
            validators=[
                IsBooleanValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"is_active2": "yes"})

    def test_is_dataclass_validator(self) -> None:
        """
        Test IsDataclassValidator.
        """

        @dataclass
        class User:
            id: int

        @dataclass
        class User2:
            name: str

        self.inputFilter.add("data", validators=[IsDataclassValidator()])

        self.inputFilter.validateData({"data": User(123)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data": "not a dataclass"})

        self.inputFilter.add(
            "data2",
            validators=[
                IsDataclassValidator(
                    User, error_message="Custom error message"
                )
            ],
        )

        self.inputFilter.validateData({"data2": User(123)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data2": User2})

    def test_is_float_validator(self) -> None:
        """
        Test that IsFloatValidator validates float type.
        """

        self.inputFilter.add("price", validators=[IsFloatValidator()])

        self.inputFilter.validateData({"price": 19.99})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"price": "not_a_float"})

        self.inputFilter.add(
            "price2",
            validators=[
                IsFloatValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"price2": "not_a_float"})

    def test_is_future_date_validator(self) -> None:
        """
        Test IsFutureDateValidator.
        """

        self.inputFilter.add("date", validators=[IsFutureDateValidator()])

        future_date = datetime.now() + timedelta(days=10)
        self.inputFilter.validateData({"date": future_date})
        future_date = (datetime.now() + timedelta(days=10)).date()
        self.inputFilter.validateData({"date": future_date})
        future_date = (datetime.now() + timedelta(days=10)).isoformat()
        self.inputFilter.validateData({"date": future_date})

        with self.assertRaises(ValidationError):
            past_date = date.today() - timedelta(days=10)
            self.inputFilter.validateData({"date": past_date})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": "not a date"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": 123})

        self.inputFilter.add(
            "date2",
            validators=[
                IsFutureDateValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            past_date = date.today() - timedelta(days=10)
            self.inputFilter.validateData({"date2": past_date})

    def test_is_hexadecimal_validator(self) -> None:
        """
        Test that HexadecimalValidator validates hexadecimal format.
        """

        self.inputFilter.add("hex", validators=[IsHexadecimalValidator()])

        self.inputFilter.validateData({"hex": "0x1234"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"hex": "not_a_hex"})

        self.inputFilter.add(
            "hex2",
            validators=[
                IsHexadecimalValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"hex2": "not_a_hex"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"hex2": 123})

    def test_is_horizontally_image_validator(self) -> None:
        """
        Test IsHorizontallyImageValidator.
        """

        self.inputFilter.add(
            "image", validators=[IsHorizontalImageValidator()]
        )

        with open("test/data/base64_image.txt", "r") as file:
            self.inputFilter.validateData({"image": file.read()})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"image": "not_a_base64_image"})

        self.inputFilter.add(
            "horizontally_image",
            filters=[
                Base64ImageDownscaleFilter(
                    width=200, height=100, proportionally=False
                )
            ],
            validators=[IsHorizontalImageValidator()],
        )

        with open("test/data/base64_image.txt", "r") as file:
            self.inputFilter.validateData({"horizontally_image": file.read()})

        self.inputFilter.add(
            "vertically_image",
            filters=[
                Base64ImageDownscaleFilter(
                    width=100, height=200, proportionally=False
                )
            ],
            validators=[IsHorizontalImageValidator()],
        )

        with open("test/data/base64_image.txt", "r") as file:
            with self.assertRaises(ValidationError):
                self.inputFilter.validateData(
                    {"vertically_image": file.read()}
                )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"vertically_image": 123})

    def test_is_instance_validator(self) -> None:
        """
        Test IsInstanceValidator.
        """

        self.inputFilter.add("user", validators=[IsInstanceValidator(dict)])

        self.inputFilter.validateData({"user": {"name": "Alice"}})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"user": "Alice"})

        self.inputFilter.add(
            "user2",
            validators=[
                IsInstanceValidator(dict, error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"user2": "Alice"})

    def test_is_integer_validator(self) -> None:
        """
        Test that IsIntegerValidator validates integer type.
        """

        self.inputFilter.add("age", validators=[IsIntegerValidator()])

        self.inputFilter.validateData({"age": 25})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"age": "obviously not an integer"})

        self.inputFilter.add(
            "age2",
            validators=[
                IsIntegerValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"age2": "obviously not an integer"})

    def test_is_json_validator(self) -> None:
        """
        Test that IsJsonValidator validates JSON format.
        """

        self.inputFilter.add("data", validators=[IsJsonValidator()])

        self.inputFilter.validateData({"data": '{"name": "Alice"}'})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data": "not_a_json"})

        self.inputFilter.add(
            "data2",
            validators=[IsJsonValidator(error_message="Custom error message")],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data2": "not_a_json"})

    def test_is_past_date_validator(self) -> None:
        """
        Test IsPastDateValidator.
        """

        self.inputFilter.add("date", validators=[IsPastDateValidator()])

        self.inputFilter.validateData({"date": date(2021, 1, 1)})
        self.inputFilter.validateData({"date": datetime(2021, 1, 1, 0, 0)})
        past_date = (datetime.now() - timedelta(days=10)).isoformat()
        self.inputFilter.validateData({"date": past_date})

        with self.assertRaises(ValidationError):
            future_date = date.today() + timedelta(days=10)
            self.inputFilter.validateData({"date": future_date})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": "not a date"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": 123})

        self.inputFilter.add(
            "date2",
            validators=[
                IsPastDateValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            future_date = date.today() + timedelta(days=10)
            self.inputFilter.validateData({"date2": future_date})

    def test_is_string_validator(self) -> None:
        """
        Test that IsStringValidator validates string type.
        """

        self.inputFilter.add("name", validators=[IsStringValidator()])

        self.inputFilter.validateData({"name": "obviously an string"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": 123})

        self.inputFilter.add(
            "name",
            validators=[
                IsStringValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": 123})

    def test_is_typed_dict_validator(self) -> None:
        """
        Test IsTypedDictValidator.
        """

        class User(TypedDict):
            id: int

        class User2(TypedDict):
            name: str

        self.inputFilter.add("data", validators=[IsTypedDictValidator()])

        self.inputFilter.validateData({"data": User(id=123)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data": "not a TypedDict"})

        self.inputFilter.add(
            "data2",
            validators=[
                IsTypedDictValidator(
                    User, error_message="Custom error message"
                )
            ],
        )

        self.inputFilter.validateData({"data2": User(id=123)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data2": User2})

    def test_is_uuid_validator(self) -> None:
        """
        Test that IsUuidValidator validates UUID format.
        """

        self.inputFilter.add("uuid", validators=[IsUUIDValidator()])

        self.inputFilter.validateData(
            {"uuid": "550e8400-e29b-41d4-a716-446655440000"}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"uuid": "not_a_uuid"})

        self.inputFilter.add(
            "uuid",
            validators=[IsUUIDValidator(error_message="Custom error message")],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"uuid": "not_a_uuid"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"uuid": 123})

    def test_is_vertically_image_validator(self) -> None:
        """
        Test IsVerticalImageValidator.
        """

        self.inputFilter.add("image", validators=[IsVerticalImageValidator()])

        with open("test/data/base64_image.txt", "r") as file:
            self.inputFilter.validateData({"image": file.read()})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"image": "not_a_base64_image"})

        self.inputFilter.add(
            "horizontally_image",
            filters=[
                Base64ImageDownscaleFilter(
                    width=200, height=100, proportionally=False
                )
            ],
            validators=[IsVerticalImageValidator()],
        )

        with open("test/data/base64_image.txt", "r") as file:
            with self.assertRaises(ValidationError):
                self.inputFilter.validateData(
                    {"horizontally_image": file.read()}
                )

        self.inputFilter.add(
            "vertically_image",
            filters=[
                Base64ImageDownscaleFilter(
                    width=100, height=200, proportionally=False
                )
            ],
            validators=[IsVerticalImageValidator()],
        )

        with open("test/data/base64_image.txt", "r") as file:
            self.inputFilter.validateData({"vertically_image": file.read()})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"vertically_image": 123})

    def test_is_weekday_validator(self) -> None:
        """
        Test IsWeekdayValidator.
        """

        self.inputFilter.add("date", validators=[IsWeekdayValidator()])

        self.inputFilter.validateData({"date": date(2021, 1, 1)})
        self.inputFilter.validateData({"date": datetime(2021, 1, 1, 11, 11)})
        self.inputFilter.validateData({"date": "2021-01-01T11:11:11"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": date(2021, 1, 2)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": "not a date"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": False})

        self.inputFilter.add(
            "date",
            validators=[
                IsWeekdayValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": date(2021, 1, 2)})

    def test_is_weekend_validator(self) -> None:
        """
        Test IsWeekendValidator.
        """

        self.inputFilter.add("date", validators=[IsWeekendValidator()])

        self.inputFilter.validateData({"date": date(2021, 1, 2)})
        self.inputFilter.validateData({"date": datetime(2021, 1, 2, 11, 11)})
        self.inputFilter.validateData({"date": "2021-01-02T11:11:11"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": date(2021, 1, 1)})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": "not a date"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": False})

        self.inputFilter.add(
            "date",
            validators=[
                IsWeekendValidator(error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"date": date(2021, 1, 1)})

    def test_length_validator(self) -> None:
        """
        Test that LengthValidator validates the length of a string.
        """

        self.inputFilter.add(
            "name",
            validators=[LengthValidator(min_length=2, max_length=5)],
        )

        self.inputFilter.validateData({"name": "test"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": "a"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": "this_is_too_long"})

        self.inputFilter.add(
            "name",
            validators=[
                LengthValidator(
                    min_length=2,
                    max_length=5,
                    error_message="Custom error message",
                )
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": "this_is_too_long"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": "a"})

    def test_not_in_array_validator(self) -> None:
        """
        Test NotInArrayValidator.
        """

        self.inputFilter.add(
            "color",
            validators=[NotInArrayValidator(["red", "green", "blue"])],
        )

        self.inputFilter.validateData({"color": "yellow"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"color": "red"})

        self.inputFilter.add(
            "color_strict",
            validators=[NotInArrayValidator(["red", "green", "blue"], True)],
        )

        self.inputFilter.validateData({"color_strict": "yellow"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"color_strict": "red"})

        self.inputFilter.add(
            "custom_error",
            validators=[
                NotInArrayValidator(
                    ["red", "green", "blue"],
                    error_message="Custom error message",
                )
            ],
        )

        self.inputFilter.validateData({"custom_error": "yellow"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"custom_error": "red"})

    def test_not_validator(self) -> None:
        """
        Test NotValidator that inverts another validator.
        """

        self.inputFilter.add(
            "age",
            validators=[NotValidator(IsIntegerValidator())],
        )

        self.inputFilter.validateData({"age": "not an integer"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"age": 25})

        self.inputFilter.add(
            "age",
            validators=[
                NotValidator(
                    IsIntegerValidator(), error_message="Custom error message"
                )
            ],
        )

        self.inputFilter.validateData({"age": "not an integer"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"age": 25})

    def test_range_validator(self) -> None:
        """
        Test that RangeValidator validates numeric values
        within a specified range.
        """

        self.inputFilter.add("range_field", validators=[RangeValidator(2, 5)])

        self.inputFilter.validateData({"name": "test", "range_field": 3.76})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"name": "test", "range_field": 1.22}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"name": "test", "range_field": 7.89}
            )

        self.inputFilter.add(
            "range_field",
            validators=[
                RangeValidator(2, 5, error_message="Custom error message")
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"name": "test", "range_field": 7.89}
            )

    def test_regex_validator(self) -> None:
        """
        Test successful validation of a valid regex format.
        """

        self.inputFilter.add(
            "email",
            validators=[
                RegexValidator(
                    RegexEnum.EMAIL.value,
                )
            ],
        )

        validated_data = self.inputFilter.validateData(
            {"email": "alice@example.com"}
        )

        self.assertEqual(validated_data["email"], "alice@example.com")

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"email": "invalid_email"})

        self.inputFilter.add(
            "email",
            validators=[
                RegexValidator(
                    RegexEnum.EMAIL.value,
                    error_message="Custom error message",
                )
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"email": "invalid_email"})


if __name__ == "__main__":
    unittest.main()

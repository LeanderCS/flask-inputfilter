import unittest
from enum import Enum

from src.flask_inputfilter.Exception import ValidationError
from src.flask_inputfilter.InputFilter import InputFilter
from src.flask_inputfilter.Validator import (
    ArrayElementValidator,
    ArrayLengthValidator,
    InArrayValidator,
    InEnumValidator,
    IsArrayValidator,
    IsBase64ImageCorrectSizeValidator,
    IsBase64ImageValidator,
    IsBooleanValidator,
    IsFloatValidator,
    IsHexadecimalValidator,
    IsInstanceValidator,
    IsIntegerValidator,
    IsJsonValidator,
    IsStringValidator,
    IsUUIDValidator,
    LengthValidator,
    RangeValidator,
    RegexValidator,
)
from src.flask_inputfilter.Validator.FloatPrecisionValidator import (
    FloatPrecisionValidator,
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
            required=True,
            validators=[IsIntegerValidator()],
        )

        self.inputFilter.add(
            "items",
            required=True,
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

    def test_array_length_validator(self) -> None:
        """
        Test ArrayLengthValidator.
        """

        self.inputFilter.add(
            "items",
            required=True,
            validators=[ArrayLengthValidator(min_length=2, max_length=5)],
        )

        self.inputFilter.validateData({"items": [1, 2, 3, 4]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"items": [1]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"items": [1, 2, 3, 4, 5, 6]})

    def test_float_precision_validator(self) -> None:
        """
        Test FloatPrecisionValidator.
        """

        self.inputFilter.add(
            "price",
            required=True,
            validators=[FloatPrecisionValidator(precision=5, scale=2)],
        )

        self.inputFilter.validateData({"price": 19.99})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"price": 19.999})

    def test_in_array_validator(self) -> None:
        """
        Test InArrayValidator.
        """

        self.inputFilter.add(
            "color",
            required=True,
            validators=[InArrayValidator(["red", "green", "blue"])],
        )

        self.inputFilter.validateData({"color": "red"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"color": "yellow"})

    def test_in_enum_validator(self) -> None:
        """
        Test InEnumValidator.
        """

        class Color(Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

        self.inputFilter.add(
            "color", required=True, validators=[InEnumValidator(Color)]
        )

        self.inputFilter.validateData({"color": "red"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"color": "yellow"})

    def test_is_array_validator(self) -> None:
        """
        Test that IsArrayValidator validates array type.
        """

        self.inputFilter.add(
            "tags", required=False, validators=[IsArrayValidator()]
        )

        self.inputFilter.validateData({"tags": ["tag1", "tag2"]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"tags": "not_an_array"})

    def test_is_base64_image_correct_size_validator(self) -> None:
        """
        Test IsBase64ImageCorrectSizeValidator.
        """

        self.inputFilter.add(
            "image",
            required=True,
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

        self.inputFilter.add(
            "is_active", required=True, validators=[IsBooleanValidator()]
        )

        self.inputFilter.validateData({"is_active": True})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"is_active": "yes"})

    def test_is_float_validator(self) -> None:
        """
        Test that IsFloatValidator validates float type.
        """

        self.inputFilter.add(
            "price", required=True, validators=[IsFloatValidator()]
        )

        self.inputFilter.validateData({"price": 19.99})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"price": "not_a_float"})

    def test_is_hexadecimal_validator(self) -> None:
        """
        Test that HexadecimalValidator validates hexadecimal format.
        """

        self.inputFilter.add(
            "hex", required=True, validators=[IsHexadecimalValidator()]
        )

        self.inputFilter.validateData({"hex": "0x1234"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"hex": "not_a_hex"})

    def test_is_instance_validator(self) -> None:
        """
        Test IsInstanceValidator.
        """

        self.inputFilter.add(
            "user", required=True, validators=[IsInstanceValidator(dict)]
        )

        self.inputFilter.validateData({"user": {"name": "Alice"}})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"user": "Alice"})

    def test_is_integer_validator(self) -> None:
        """
        Test that IsIntegerValidator validates integer type.
        """

        self.inputFilter.add(
            "age", required=True, validators=[IsIntegerValidator()]
        )

        self.inputFilter.validateData({"age": 25})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"age": "obviously not an integer"})

    def test_is_json_validator(self) -> None:
        """
        Test that IsJsonValidator validates JSON format.
        """

        self.inputFilter.add(
            "data", required=True, validators=[IsJsonValidator()]
        )

        self.inputFilter.validateData({"data": '{"name": "Alice"}'})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"data": "not_a_json"})

    def test_is_string_validator(self) -> None:
        """
        Test that IsStringValidator validates string type.
        """

        self.inputFilter.add(
            "name", required=True, validators=[IsStringValidator()]
        )

        self.inputFilter.validateData({"name": "obviously an string"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": 123})

    def test_is_uuid_validator(self) -> None:
        """
        Test that IsUuidValidator validates UUID format.
        """

        self.inputFilter.add(
            "uuid", required=True, validators=[IsUUIDValidator()]
        )

        self.inputFilter.validateData(
            {"uuid": "550e8400-e29b-41d4-a716-446655440000"}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"uuid": "not_a_uuid"})

    def test_length_validator(self) -> None:
        """
        Test that LengthValidator validates the length of a string.
        """

        self.inputFilter.add(
            "name",
            required=False,
            validators=[LengthValidator(min_length=2, max_length=5)],
        )

        self.inputFilter.validateData({"name": "test"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": "a"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": "this_is_too_long"})

    def test_range_validator(self) -> None:
        """
        Test that RangeValidator validates numeric values within a specified range.
        """

        self.inputFilter.add(
            "range_field", required=False, validators=[RangeValidator(2, 5)]
        )

        self.inputFilter.validateData({"name": "test", "range_field": 3.76})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"name": "test", "range_field": 1.22}
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
            required=False,
            validators=[RegexValidator(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")],
        )

        validated_data = self.inputFilter.validateData(
            {"email": "alice@example.com"}
        )

        self.assertEqual(validated_data["email"], "alice@example.com")

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"email": "invalid_email"})

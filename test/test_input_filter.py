import unittest

from src.flask_inputfilter.Exception import ValidationError
from src.flask_inputfilter.InputFilter import InputFilter
from src.flask_inputfilter.Validator import InArrayValidator


class TestInputFilter(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up a basic InputFilter instance for testing.
        """

        self.inputFilter = InputFilter()

    def test_optional(self) -> None:
        """
        Test that optional field validation works.
        """

        self.inputFilter.add("name", required=True)

        self.inputFilter.validateData({"name": "Alice"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({})

    def test_default(self) -> None:
        """
        Test that default field works.
        """

        self.inputFilter.add("available", required=False, default=True)

        # Default case triggert
        validated_data = self.inputFilter.validateData({})

        self.assertEqual(validated_data["available"], True)

        # Override default case
        validated_data = self.inputFilter.validateData({"available": False})

        self.assertEqual(validated_data["available"], False)

    def test_fallback(self) -> None:
        """
        Test that fallback field works.
        """

        self.inputFilter.add("available", required=True, fallback=True)
        self.inputFilter.add(
            "color",
            required=False,
            fallback="red",
            validators=[InArrayValidator(["red", "green", "blue"])],
        )

        # Fallback case triggert
        validated_data = self.inputFilter.validateData({"color": "yellow"})

        self.assertEqual(validated_data["available"], True)
        self.assertEqual(validated_data["color"], "red")

        # Override fallback case
        validated_data = self.inputFilter.validateData(
            {"available": False, "color": "green"}
        )

        self.assertEqual(validated_data["available"], False)
        self.assertEqual(validated_data["color"], "green")

import unittest

from src.flask_inputfilter import InputFilter
from src.flask_inputfilter.Condition import (
    ArrayLengthEqualCondition,
    ArrayLongerThanCondition,
    CustomCondition,
    EqualCondition,
    ExactlyNOfCondition,
    ExactlyNOfMatchesCondition,
    ExactlyOneOfCondition,
    ExactlyOneOfMatchesCondition,
    IntegerBiggerThanCondition,
    NOfCondition,
    NOfMatchesCondition,
    OneOfCondition,
    OneOfMatchesCondition,
    RequiredIfCondition,
    StringLongerThanCondition,
)
from src.flask_inputfilter.Exception import ValidationError


class TestConditions(unittest.TestCase):
    def setUp(self):
        """
        Set up test data.
        """

        self.inputFilter = InputFilter()

    def test_array_length_equal_condition(self) -> None:
        """
        Test ArrayLengthEqualCondition.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            ArrayLengthEqualCondition("field1", "field2")
        )

        self.inputFilter.validateData({"field1": [1, 2], "field2": [1, 2]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": [1, 2]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": [1, 2], "field2": [1]})

    def test_array_longer_than_condition(self) -> None:
        """
        Test ArrayLongerThanCondition.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            ArrayLongerThanCondition("field1", "field2")
        )

        self.inputFilter.validateData({"field1": [1, 2], "field2": [1]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": [1, 2], "field2": [1, 2]})

    def test_custom_condition(self) -> None:
        """
        Test CustomCondition.
        """

        self.inputFilter.add("field")

        self.inputFilter.addCondition(
            CustomCondition(
                lambda data: "field" in data and data["field"] == "value"
            )
        )

        self.inputFilter.validateData({"field": "value"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({})

    def test_equal_condition(self) -> None:
        """
        Test EqualCondition.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(EqualCondition("field1", "field2"))

        self.inputFilter.validateData({})
        self.inputFilter.validateData({"field1": "value", "field2": "value"})
        self.inputFilter.validateData({"field1": True, "field2": True})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "value", "field2": "not value"}
            )

    def test_exactly_nth_of_condition(self) -> None:
        """
        Test NthOfCondition when exactly one field is present.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            ExactlyNOfCondition(["field1", "field2", "field3"], 1)
        )

        self.inputFilter.validateData({"field1": "value"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "value", "field2": "value"}
            )

    def test_exactly_nth_of_matches_condition(self) -> None:
        """
        Test NthOfMatchesCondition when exactly one field matches the value.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")
        self.inputFilter.add("field3")

        self.inputFilter.addCondition(
            ExactlyNOfMatchesCondition(
                ["field1", "field2", "field3"], 2, "value"
            )
        )

        self.inputFilter.validateData({"field1": "value", "field2": "value"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": "value"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "value", "field2": "value", "field3": "value"}
            )

    def test_exactly_one_of_condition(self) -> None:
        """
        Test OneOfCondition when exactly one field is present.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            ExactlyOneOfCondition(["field1", "field2", "field3"])
        )

        self.inputFilter.validateData({"field1": "value"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "value", "field2": "value"}
            )

    def test_exactly_one_of_matches_condition(self) -> None:
        """
        Test OneOfMatchesCondition when exactly one field matches the value.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], "value")
        )

        self.inputFilter.validateData({"field1": "value"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "value", "field2": "value"}
            )

    def test_integer_bigger_than_condition(self) -> None:
        """
        Test IntegerBiggerThanCondition.
        """

        self.inputFilter.add("field")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            IntegerBiggerThanCondition("field", "field2")
        )

        self.inputFilter.validateData({"field": 11, "field2": 10})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field": 10, "field2": 10})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field": 10, "field2": 11})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field": 10})

    def test_nth_of_condition(self) -> None:
        """
        Test NthOfCondition when exactly one field is present.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            NOfCondition(["field1", "field2", "field3"], 2)
        )

        self.inputFilter.validateData({"field1": "value", "field2": "value"})
        self.inputFilter.validateData(
            {"field1": "value", "field2": "value", "field3": "value"}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": "value"})

    def test_nth_of_matches_condition(self) -> None:
        """
        Test NthOfMatchesCondition when exactly one field matches the value.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")
        self.inputFilter.add("field3")
        self.inputFilter.add("field4")

        self.inputFilter.addCondition(
            NOfMatchesCondition(["field1", "field2", "field3"], 3, "value")
        )

        self.inputFilter.validateData(
            {"field1": "value", "field2": "value", "field3": "value"}
        )

        self.inputFilter.validateData(
            {
                "field1": "value",
                "field2": "value",
                "field3": "value",
                "field4": "value",
            }
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "value", "field2": "value"}
            )

    def test_one_of_condition(self) -> None:
        """
        Test OneOfCondition when at least one field is present.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            OneOfCondition(["field1", "field2", "field3"])
        )

        self.inputFilter.validateData({"field1": "value"})
        self.inputFilter.validateData({"field2": "value"})
        self.inputFilter.validateData({"field1": "value", "field2": "value"})
        self.inputFilter.validateData(
            {"field": "not value", "field2": "value"}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({})

    def test_one_of_matches_condition(self) -> None:
        """
        Test OneOfMatchesCondition when at least one field matches the value.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            OneOfMatchesCondition(["field1", "field2"], "value")
        )

        self.inputFilter.validateData({"field1": "value"})
        self.inputFilter.validateData({"field2": "value"})
        self.inputFilter.validateData({"field1": "value", "field2": "value"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field": "not value"})

    def test_required_if_condition(self) -> None:
        """
        Test RequiredIfCondition.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            RequiredIfCondition("field1", "value", "field2")
        )

        self.inputFilter.validateData({"field2": "value"})
        self.inputFilter.validateData({"field1": "value", "field2": "value"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": "value"})

    def test_string_longer_than_condition(self) -> None:
        """
        Test StringLongerThanCondition.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            StringLongerThanCondition("field1", "field2")
        )

        self.inputFilter.validateData({"field1": "value", "field2": "val"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "value", "field2": "value"}
            )


if __name__ == "__main__":
    unittest.main()

import unittest
from datetime import date, datetime

from flask_inputfilter import InputFilter
from flask_inputfilter.Condition import (
    ArrayLengthEqualCondition,
    ArrayLongerThanCondition,
    BaseCondition,
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
    TemporalOrderCondition,
)
from flask_inputfilter.Condition.NotEqualCondition import NotEqualCondition
from flask_inputfilter.Exception import ValidationError


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

        self.inputFilter.validateData({"field1": [], "field2": []})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": [1, 2]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": [1, 2], "field2": [1]})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": [1, 2], "field2": [1, 2, 3]}
            )

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

    def test_base_condition(self) -> None:
        """
        Test BaseCondition.
        """

        with self.assertRaises(TypeError):
            BaseCondition().check({})

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

    def test_not_equal_condition(self) -> None:
        """
        Test NotEqualCondition.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(NotEqualCondition("field1", "field2"))

        self.inputFilter.validateData(
            {"field1": "value", "field2": "not value"}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "value", "field2": "value"}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "value", "field2": "value"}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": True, "field2": True})

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

        # Case 1: value is a single value
        self.inputFilter.addCondition(
            RequiredIfCondition("field1", "value", "field2")
        )

        self.inputFilter.validateData({"field1": "not value"})
        self.inputFilter.validateData({"field2": "value"})
        self.inputFilter.validateData(
            {"field1": "value", "field2": "other value"}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": "value"})

        # Case 2: value is a list
        self.inputFilter.add("field3")
        self.inputFilter.add("field4")

        self.inputFilter.addCondition(
            RequiredIfCondition("field3", ["value1", "value2"], "field4")
        )

        self.inputFilter.validateData({"field4": "value2"})
        self.inputFilter.validateData({"field3": "value1", "field4": "value"})
        self.inputFilter.validateData({"field3": "value2", "field4": "value"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field3": "value1"})

        # Case 3: value is None
        self.inputFilter.add("field5")
        self.inputFilter.add("field6")
        self.inputFilter.addCondition(
            RequiredIfCondition("field5", None, "field6")
        )

        self.inputFilter.validateData({"field6": "value"})
        self.inputFilter.validateData(
            {"field5": "any_value", "field6": "value"}
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field5": "any_value"})

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

    def test_temporal_order_condition(self) -> None:
        """
        Test TemporalOrderCondition.
        """

        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addCondition(
            TemporalOrderCondition("field1", "field2")
        )

        self.inputFilter.validateData(
            {"field1": "2021-01-01", "field2": "2021-01-02"}
        )

        self.inputFilter.validateData(
            {
                "field1": datetime(2021, 1, 1, 12, 0, 0),
                "field2": datetime(2021, 1, 2, 12, 0, 0),
            }
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": "2021-01-02", "field2": "2021-01-01"}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"field1": date(2023, 1, 1), "field2": "2021-01-01"}
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": "2021-01-01"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {
                    "field1": datetime(2021, 1, 1, 12, 0, 0),
                    "field2": datetime(2020, 1, 1, 12, 0, 0),
                }
            )

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": "not a datetime"})


if __name__ == "__main__":
    unittest.main()

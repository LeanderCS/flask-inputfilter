import unittest

from flask_inputfilter.models import BaseCondition


class TestBaseCondition(unittest.TestCase):
    def test_raises_error_when_check_called(self) -> None:
        """Test that BaseCondition raises a TypeError."""
        with self.assertRaises(NotImplementedError):
            BaseCondition().check({})

    def test_raises_error_with_none_data(self) -> None:
        """Test that BaseCondition raises NotImplementedError with None
        data."""
        with self.assertRaises(NotImplementedError):
            BaseCondition().check(None)

    def test_raises_error_with_populated_data(self) -> None:
        """Test that BaseCondition raises NotImplementedError with populated
        data."""
        with self.assertRaises(NotImplementedError):
            BaseCondition().check({"field": "value"})

    def test_raises_error_with_complex_data(self) -> None:
        """Test that BaseCondition raises NotImplementedError with complex
        data."""
        with self.assertRaises(NotImplementedError):
            BaseCondition().check(
                {
                    "field1": "value1",
                    "field2": 123,
                    "field3": None,
                    "field4": [],
                    "field5": {},
                }
            )

    def test_raises_error_with_nested_data(self) -> None:
        """Test that BaseCondition raises NotImplementedError with nested
        data."""
        with self.assertRaises(NotImplementedError):
            BaseCondition().check(
                {"field": {"nested": "value"}, "array": [1, 2, 3]}
            )

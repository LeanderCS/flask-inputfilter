import unittest

from flask_inputfilter.conditions import BaseCondition


class TestBaseCondition(unittest.TestCase):
    def test_raises_error_when_check_called(self) -> None:
        """Test that BaseCondition raises a TypeError."""
        with self.assertRaises(TypeError):
            BaseCondition().check({})

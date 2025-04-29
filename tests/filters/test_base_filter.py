import unittest

from flask_inputfilter.filters import BaseFilter


class TestBaseFilter(unittest.TestCase):
    def test_apply_raises_type_error(self) -> None:
        """Should raise TypeError when calling apply on BaseFilter directly."""
        with self.assertRaises(TypeError):
            BaseFilter().apply("test")

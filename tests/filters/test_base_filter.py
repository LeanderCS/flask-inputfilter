import unittest

from flask_inputfilter.models import BaseFilter


class TestBaseFilter(unittest.TestCase):
    def test_apply_raises_type_error(self) -> None:
        """Should raise TypeError when calling apply on BaseFilter directly."""
        with self.assertRaises(NotImplementedError):
            BaseFilter().apply("test")

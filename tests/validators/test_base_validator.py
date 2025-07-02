import unittest

from flask_inputfilter.models import BaseValidator


class TestBaseValidator(unittest.TestCase):
    def test_validate_method_raises_type_error(self) -> None:
        with self.assertRaises(NotImplementedError):
            BaseValidator().validate("value")

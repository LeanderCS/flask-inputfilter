import unittest

from flask_inputfilter.validators import BaseValidator


class TestBaseValidator(unittest.TestCase):
    def test_validate_method_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            BaseValidator().validate("value")

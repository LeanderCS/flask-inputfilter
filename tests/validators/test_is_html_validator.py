import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsHtmlValidator


class TestIsHtmlValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_html(self) -> None:
        self.input_filter.add("html_content", validators=[IsHtmlValidator()])
        self.input_filter.validateData({"html_content": "<div>Hello</div>"})

    def test_invalid_html(self) -> None:
        self.input_filter.add("html_content", validators=[IsHtmlValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"html_content": "no html here"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "html_content2",
            validators=[IsHtmlValidator(error_message="Custom error")],
        )
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"html_content2": "no html"})
        self.assertEqual(
            context.exception.args[0]["html_content2"], "Custom error"
        )

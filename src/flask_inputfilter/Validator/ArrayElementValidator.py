from typing import Any, TYPE_CHECKING

from src.flask_inputfilter.Exception import ValidationError
from ..Validator.BaseValidator import BaseValidator


if TYPE_CHECKING:
    from src.flask_inputfilter.InputFilter import InputFilter


class ArrayElementValidator(BaseValidator):
    """
    Validator to validate each element in an array.
    """

    def __init__(self, elementFilter: 'InputFilter') -> None:

        self.elementFilter = elementFilter

    def validate(self, value: Any) -> None:

        if not isinstance(value, list):
            raise ValidationError("Value is not an array")

        for i, element in enumerate(value):
            try:
                validated_element = self.elementFilter.validateData(element)
                value[i] = validated_element

            except ValidationError:
                raise ValidationError(f"Invalid element '{element}' in array")

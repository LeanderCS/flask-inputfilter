from typing import TYPE_CHECKING, Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator

if TYPE_CHECKING:
    from flask_inputfilter import InputFilter


class ArrayElementValidator(BaseValidator):
    """
    Validator to validate each element in an array.
    """

    def __init__(
        self,
        elementFilter: "InputFilter",
        error_message: Optional[str] = None,
    ) -> None:
        self.elementFilter = elementFilter
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, list):
            raise ValidationError(f"Value '{value}' is not an array")

        for i, element in enumerate(value):
            try:
                validated_element = self.elementFilter.validateData(element)
                value[i] = validated_element

            except ValidationError:
                raise ValidationError(
                    self.error_message
                    or f"Value '{element}' is not in '{self.elementFilter}'"
                )

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator

if TYPE_CHECKING:
    from flask_inputfilter import InputFilter


class ArrayElementValidator(BaseValidator):
    """
    Validator to validate each element in an array.
    """

    __slots__ = ("elementFilter", "error_message")

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
                value[i] = deepcopy(self.elementFilter.validateData(element))

            except ValidationError:
                raise ValidationError(
                    self.error_message
                    or f"Value '{element}' is not in '{self.elementFilter}'"
                )

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, Dict, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator

if TYPE_CHECKING:
    from flask_inputfilter import InputFilter


class ArrayElementValidator(BaseValidator):
    """
    Validates each element within an array by applying an inner ``InputFilter``
    to every element. It ensures that all array items conform to the expected
    structure.

    **Parameters:**

    - **elementFilter** (*InputFilter*): An instance used to validate
        each element.
    - **error_message** (*Optional[str]*): Custom error message for
        validation failure.

    **Expected Behavior:**

    Verifies that the input is a list and then applies the provided filter
    to each element. If any element fails validation, a ``ValidationError``
    is raised.

    **Example Usage:**

    .. code-block:: python

        from my_filters import MyElementFilter

        class TagInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('tags', validators=[
                    ArrayElementValidator(elementFilter=MyElementFilter())
                ])
    """

    __slots__ = ("element_filter", "error_message")

    def __init__(
        self,
        elementFilter: "InputFilter",
        error_message: Optional[str] = None,
    ) -> None:
        self.element_filter = elementFilter
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, list):
            raise ValidationError(f"Value '{value}' is not an array")

        for i, element in enumerate(value):
            try:
                if not isinstance(element, Dict):
                    raise ValidationError

                value[i] = deepcopy(self.element_filter.validateData(element))

            except ValidationError:
                raise ValidationError(
                    self.error_message
                    or f"Value '{element}' is not in '{self.element_filter}'"
                )

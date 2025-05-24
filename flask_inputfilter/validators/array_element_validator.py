from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

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

    - **elementFilter** (*InputFilter* | *BaseValidator* |
        *list[BaseValidator]*): An instance used to validate each element.
    - **error_message** (*Optional[str]*): Custom error message for validation
        failure.

    **Expected Behavior:**

    Verifies that the input is a list and then applies the provided filter
    to each element. If any element fails validation, a ``ValidationError``
    is raised.

    **Example Usage:**

    This example demonstrates how to use the `ArrayElementValidator` with a
    custom `InputFilter` for validating elements in an array.

    .. code-block:: python

        from my_filters import UserInputFilter

        class UsersInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('users', validators=[
                    ArrayElementValidator(element_filter=UserInputFilter())
                ])

    Additionally, you can use a validator directly on your elements:

    .. code-block:: python

        class TagInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('tags', validators=[
                    ArrayElementValidator(element_filter=IsStringValidator())
                ])
    """

    __slots__ = ("element_filter", "error_message")

    def __init__(
        self,
        element_filter: Union[
            "InputFilter", BaseValidator, List[BaseValidator]
        ],
        error_message: Optional[str] = None,
    ) -> None:
        self.element_filter = element_filter
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, list):
            raise ValidationError(f"Value '{value}' is not an array")

        for i, element in enumerate(value):
            try:
                if isinstance(self.element_filter, BaseValidator):
                    self.element_filter.validate(element)
                    value[i] = element
                    continue

                elif isinstance(self.element_filter, list) and all(
                    isinstance(v, BaseValidator) for v in self.element_filter
                ):
                    for validator in self.element_filter:
                        validator.validate(element)
                    value[i] = element
                    continue

                if not isinstance(element, Dict):
                    raise ValidationError(
                        f"Element is not a dictionary: {element}"
                    )

                value[i] = deepcopy(self.element_filter.validate_data(element))

            except ValidationError as e:
                raise ValidationError(self.error_message or str(e))

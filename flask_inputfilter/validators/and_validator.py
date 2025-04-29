from __future__ import annotations

from typing import Any, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class AndValidator(BaseValidator):
    """
    Validates that the input passes all the provided validators. This composite
    validator performs a logical AND over its constituent validators.

    **Parameters:**

    - **validators** (*List[BaseValidator]*): A list of validators that must
        all pass.
    - **error_message** (*Optional[str]*): Custom error message if any of the
        validators fail.

    **Expected Behavior:**

    The validator sequentially applies each validator in the provided list to
    the input value. If any validator raises a ``ValidationError``, the
    AndValidator immediately raises a ``ValidationError``. If all validators
    pass, the input is considered valid.

    **Example Usage:**

    .. code-block:: python

        class AndInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('value', validators=[
                    AndValidator([
                        IsIntegerValidator(),
                        RangeValidator(min_value=0, max_value=100)
                    ])
                ])
    """

    __slots__ = ("validators", "error_message")

    def __init__(
        self,
        validators: List[BaseValidator],
        error_message: Optional[str] = None,
    ) -> None:
        self.validators = validators
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        for validator in self.validators:
            try:
                validator.validate(value)

            except ValidationError as e:
                raise ValidationError(self.error_message or e)

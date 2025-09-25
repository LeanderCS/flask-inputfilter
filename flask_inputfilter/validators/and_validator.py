from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class AndValidator(BaseValidator):
    """
    Validates that the input passes all the provided validators. This composite
    validator performs a logical AND over its constituent validators.

    **Parameters:**

    - **validators** (*list[BaseValidator]*): A list of validators that must
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
            value: int = field(validators=[
                AndValidator([
                    IsIntegerValidator(),
                    RangeValidator(min_value=0, max_value=100)
                ])
            ])
    """

    __slots__ = ("error_message", "validators")

    def __init__(
        self,
        validators: list[BaseValidator],
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

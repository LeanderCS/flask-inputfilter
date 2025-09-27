from __future__ import annotations

from typing import TYPE_CHECKING

from ._utils import append_to_class_list

if TYPE_CHECKING:
    from flask_inputfilter.models import BaseValidator


def global_validator(*validator_instances: BaseValidator) -> None:
    """
    Register one or more global validators for declarative definition.

    This function registers global validators directly in the class definition
    without requiring variable assignment or __init__ methods.

    **Parameters:**

    - **validator_instances** (*BaseValidator*): One or more validator
      instances to register globally.

    **Examples:**

    .. code-block:: python

        class MyInputFilter(InputFilter):
            name: str = field(required=True)
            email: str = field(required=True)

            # Single global validator
            global_validator(IsStringValidator())

            # Multiple global validators at once
            global_validator(
                IsStringValidator(),
                LengthValidator(min_length=1),
                NotEmptyValidator()
            )
    """
    for validator_instance in validator_instances:
        append_to_class_list("_global_validators", validator_instance)

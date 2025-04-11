from typing import Any, List

from typing_extensions import final

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Mixin import BaseMixin
from flask_inputfilter.Validator import BaseValidator


class ValidationMixin(BaseMixin):
    @final
    def addGlobalValidator(self, validator: BaseValidator) -> None:
        """
        Add a global validator to be applied to all fields.

        Args:
            validator: The validator to add.
        """
        self._global_validators.append(validator)

    @final
    def getGlobalValidators(self) -> List[BaseValidator]:
        """
        Retrieve all global validators associated with this
        InputFilter instance.

        This method returns a list of BaseValidator instances that have been
        added as global validators. These validators are applied universally
        to all fields during validation.

        Returns:
            List[BaseValidator]: A list of global validators.
        """
        return self._global_validators

    def __validateField(
        self, validators: List[BaseValidator], fallback: Any, value: Any
    ) -> None:
        """
        Validate the field value.
        """
        if value is None:
            return

        try:
            for validator in self._global_validators + validators:
                validator.validate(value)
        except ValidationError:
            if fallback is None:
                raise

            return fallback

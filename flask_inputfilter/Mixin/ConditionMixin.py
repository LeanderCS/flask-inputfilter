from typing import Any, Dict, List

from typing_extensions import final

from flask_inputfilter.Condition import BaseCondition
from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Mixin import BaseMixin


class ConditionMixin(BaseMixin):
    @final
    def addCondition(self, condition: BaseCondition) -> None:
        """
        Add a condition to the input filter.

        Args:
            condition: The condition to add.
        """
        self._conditions.append(condition)

    @final
    def getConditions(self) -> List[BaseCondition]:
        """
        Retrieve the list of all registered conditions.

        This function provides access to the conditions that have been
        registered and stored. Each condition in the returned list
        is represented as an instance of the BaseCondition type.

        Returns:
            List[BaseCondition]: A list containing all currently registered
                instances of BaseCondition.
        """
        return self._conditions

    def __checkConditions(self, validated_data: Dict[str, Any]) -> None:
        for condition in self._conditions:
            if not condition.check(validated_data):
                raise ValidationError(
                    f"Condition '{condition.__class__.__name__}' not met."
                )

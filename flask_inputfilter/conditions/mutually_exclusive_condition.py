from __future__ import annotations

"""Mutually exclusive fields condition."""

from typing import Any, Dict, List, Optional

from flask_inputfilter.models import BaseCondition


class MutuallyExclusiveCondition(BaseCondition):
    """
    Ensures that fields are mutually exclusive.

    This condition validates that only one group of fields from multiple groups
    can be present at the same time.
    """

    def __init__(
        self,
        field_groups: List[List[str]],
        require_one: bool = True,
        allow_none: bool = False,
        custom_message: Optional[str] = None,
    ) -> None:
        """
        Initialize the mutually exclusive condition.

        Args:
            field_groups: List of field groups that are mutually exclusive
            require_one: Whether exactly one group must be present
            allow_none: Whether all groups can be absent
            custom_message: Custom error message

        Example:
            # Either username/password OR api_key, but not both
            MutuallyExclusiveCondition([
                ['username', 'password'],
                ['api_key']
            ])
        """
        self.field_groups = field_groups
        self.require_one = require_one
        self.allow_none = allow_none
        self.custom_message = custom_message

    def check(self, data: Dict[str, Any]) -> bool:
        """
        Check if the mutually exclusive condition is met.

        Args:
            data: The validated data dictionary

        Returns:
            True if condition is met, False otherwise
        """
        if not isinstance(data, dict):
            return False

        groups_present = 0
        groups_info = []

        for group in self.field_groups:
            group_fields_present = []
            for field in group:
                if field in data and data[field] is not None:
                    if isinstance(data[field], str) and data[field] == "":
                        continue
                    group_fields_present.append(field)

            if group_fields_present:
                groups_present += 1
                groups_info.append(group_fields_present)

        if groups_present > 1:
            return False

        if groups_present == 0:
            return self.allow_none

        return True

    def get_error_message(self, data: Dict[str, Any]) -> str:
        """
        Get a descriptive error message.

        Args:
            data: The validated data dictionary

        Returns:
            Error message string
        """
        if self.custom_message:
            return self.custom_message

        present_groups = []
        for i, group in enumerate(self.field_groups):
            group_fields = [
                f for f in group if f in data and data[f] is not None
            ]
            if group_fields:
                present_groups.append(
                    f"Group {i + 1}: {', '.join(group_fields)}"
                )

        if len(present_groups) > 1:
            return (
                f"Fields are mutually exclusive. "
                f"Only one group can be present, but found: {'; '.join(present_groups)}"
            )

        if len(present_groups) == 0 and self.require_one:
            group_descriptions = []
            for i, group in enumerate(self.field_groups):
                group_descriptions.append(f"Group {i + 1}: {', '.join(group)}")
            return (
                f"At least one group of fields must be present. "
                f"Available groups: {'; '.join(group_descriptions)}"
            )

        return "Mutually exclusive condition not met"

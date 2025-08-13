from __future__ import annotations

from typing import Any, Dict, List, Optional

from flask_inputfilter.models import BaseCondition


class AtLeastOneRequiredCondition(BaseCondition):
    """
    Ensures that at least one field from a list is present.

    This condition validates that at least one field from a specified list of
    fields is present and has a non-empty value.
    """

    def __init__(
        self,
        fields: List[str],
        min_required: int = 1,
        check_empty: bool = True,
        custom_message: Optional[str] = None,
    ) -> None:
        """
        Initialize the at least one required condition.

        Args:
            fields: List of field names to check
            min_required: Minimum number of fields that must be present
            check_empty: Whether to consider empty strings as absent
            custom_message: Custom error message

        Example:
            # At least one contact method required
            AtLeastOneRequiredCondition(['email', 'phone', 'address'])
        """
        self.fields = fields
        self.min_required = min_required
        self.check_empty = check_empty
        self.custom_message = custom_message

    def check(self, data: Dict[str, Any]) -> bool:
        """
        Check if at least the minimum required fields are present.

        Args:
            data: The validated data dictionary

        Returns:
            True if condition is met, False otherwise
        """
        if not isinstance(data, dict):
            return False

        present_count = 0

        for field in self.fields:
            if field in data and data[field] is not None:
                if (
                    self.check_empty
                    and isinstance(data[field], str)
                    and data[field].strip() == ""
                ):
                    continue

                if (
                    self.check_empty
                    and isinstance(data[field], (list, dict))
                    and len(data[field]) == 0
                ):
                    continue

                present_count += 1

        return present_count >= self.min_required

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

        present_fields = []
        missing_fields = []

        for field in self.fields:
            if field in data and data[field] is not None:
                if self.check_empty:
                    if (
                        isinstance(data[field], str)
                        and data[field].strip() == ""
                    ) or (
                        isinstance(data[field], (list, dict))
                        and len(data[field]) == 0
                    ):
                        missing_fields.append(field)
                    else:
                        present_fields.append(field)
                else:
                    present_fields.append(field)
            else:
                missing_fields.append(field)

        if self.min_required == 1:
            fields_list = ", ".join(self.fields)
            return (
                f"At least one of the following fields is required: {fields_list}. "
                f"None were provided or all were empty."
            )
        fields_list = ", ".join(self.fields)
        return (
            f"At least {self.min_required} of the following fields "
            f"are required: {fields_list}. Only {len(present_fields)} provided."
        )

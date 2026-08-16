"""Validator formatter for generating Python code from validator
configurations."""

from __future__ import annotations

from typing import Any


def _format_list(items: list[Any]) -> str:
    """Format a list for Python code."""
    return "[" + ", ".join(repr(item) for item in items) + "]"


class ValidatorFormatter:
    """Formats validator configurations into Python code strings."""

    @staticmethod
    def format(validator_config: dict[str, Any]) -> str:
        """
        Format a validator configuration into Python code.

        Args:
            validator_config: Dictionary with validator type and parameters.

        Returns:
            Python code string for the validator.
        """
        validator_type = validator_config.get("type")
        if not validator_type:
            return ""

        if validator_type in ("LengthValidator", "ArrayLengthValidator"):
            return ValidatorFormatter._format_length_validator(
                validator_config
            )
        if validator_type == "RangeValidator":
            return ValidatorFormatter._format_range_validator(validator_config)
        if validator_type == "RegexValidator":
            return ValidatorFormatter._format_regex_validator(validator_config)
        if validator_type == "InArrayValidator":
            return ValidatorFormatter._format_in_array_validator(
                validator_config
            )
        if validator_type == "ArrayElementValidator":
            return ValidatorFormatter._format_array_element_validator(
                validator_config
            )
        return ValidatorFormatter._format_simple_validator(validator_config)

    @staticmethod
    def _format_length_validator(config: dict[str, Any]) -> str:
        """Format LengthValidator or ArrayLengthValidator."""
        validator_type = config.get("type")
        min_len = config.get("min_length")
        max_len = config.get("max_length")
        args = []
        if min_len is not None:
            args.append(f"min_length={min_len}")
        if max_len is not None:
            args.append(f"max_length={max_len}")
        return (
            f"{validator_type}({', '.join(args)})"
            if args
            else f"{validator_type}()"
        )

    @staticmethod
    def _format_range_validator(config: dict[str, Any]) -> str:
        """Format RangeValidator."""
        min_val = config.get("min_value")
        max_val = config.get("max_value")
        args = []
        if min_val is not None:
            args.append(f"min_value={min_val}")
        if max_val is not None:
            args.append(f"max_value={max_val}")
        return (
            f"RangeValidator({', '.join(args)})"
            if args
            else "RangeValidator()"
        )

    @staticmethod
    def _format_regex_validator(config: dict[str, Any]) -> str:
        """Format RegexValidator."""
        pattern = config.get("pattern")
        if pattern:
            return f"RegexValidator(pattern={pattern!r})"
        return "RegexValidator()"

    @staticmethod
    def _format_in_array_validator(config: dict[str, Any]) -> str:
        """Format InArrayValidator."""
        haystack = config.get("haystack", [])
        haystack_str = _format_list(haystack)
        return f"InArrayValidator(haystack={haystack_str})"

    @staticmethod
    def _format_array_element_validator(config: dict[str, Any]) -> str:
        """Format ArrayElementValidator."""
        element_filter = config.get("element_filter", [])
        if isinstance(element_filter, str) and element_filter:
            return f"ArrayElementValidator(element_filter={element_filter}())"
        if isinstance(element_filter, list) and element_filter:
            element_validators = []
            for elem_val in element_filter:
                if isinstance(elem_val, dict):
                    elem_type = elem_val.get("type")
                    if elem_type == "RegexValidator":
                        pattern = elem_val.get("pattern")
                        if pattern:
                            element_validators.append(
                                f"RegexValidator(pattern={pattern!r})"
                            )
                    else:
                        element_validators.append(f"{elem_type}()")
            if element_validators:
                joined = ", ".join(element_validators)
                return f"ArrayElementValidator(element_filter=[{joined}])"
        return "ArrayElementValidator()"

    @staticmethod
    def _format_simple_validator(config: dict[str, Any]) -> str:
        """Format simple validators without special parameters."""
        validator_type = config.get("type")
        return f"{validator_type}()"

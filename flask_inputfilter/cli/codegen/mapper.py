from __future__ import annotations

import json
from typing import Any, Dict, List, Set


class TypeMapper:
    """Enhanced mapping from JSON Schema types to Flask InputFilter
    components."""

    FILTERS = {
        "string": ["StringTrimFilter"],
        "integer": [],
        "number": ["ToFloatFilter"],
        "boolean": [],
    }

    FORMAT_VALIDATORS = {
        "email": "RegexValidator(RegexEnum.EMAIL.value, 'Invalid email format.')",
        "uri": "RegexValidator(RegexEnum.URL.value, 'Invalid URL format.')",
        "uuid": "IsUUIDValidator()",
        "date": "IsDateValidator()",
        "date-time": "IsDateTimeValidator()",
        "ipv4": "RegexValidator(RegexEnum.IPV4.value, 'Invalid IPv4 address.')",
        "ipv6": "RegexValidator(RegexEnum.IPV6.value, 'Invalid IPv6 address.')",
    }

    TYPE_VALIDATORS = {
        "string": "IsStringValidator()",
        "integer": "IsIntegerValidator()",
        "number": "IsFloatValidator()",
        "boolean": "IsBooleanValidator()",
        "array": "IsArrayValidator()",
    }

    def __init__(self) -> None:
        self.import_filters: Set[str] = set()
        self.import_validators: Set[str] = set()
        self.import_enums: Set[str] = set()

    def map_field(
        self, attr: str, spec: Dict[str, Any], required_fields: Set[str]
    ) -> dict:
        """Map a single field from JSON schema to InputFilter field
        definition."""
        filters: List[str] = []
        validators: List[str] = []

        field_type = spec.get("type")
        field_format = spec.get("format")

        # Add type-specific filters
        for f in self.FILTERS.get(field_type, []):
            filters.append(f"{f}()")
            self.import_filters.add(f)

        # Add format-specific validators
        if field_format and field_format in self.FORMAT_VALIDATORS:
            validator_def = self.FORMAT_VALIDATORS[field_format]
            validators.append(validator_def)

            # Extract validator class names for imports
            if "RegexValidator" in validator_def:
                self.import_validators.add("RegexValidator")
                self.import_enums.add("RegexEnum")
            elif "IsUUIDValidator" in validator_def:
                self.import_validators.add("IsUUIDValidator")
            elif "IsDateValidator" in validator_def:
                self.import_validators.add("IsDateValidator")
            elif "IsDateTimeValidator" in validator_def:
                self.import_validators.add("IsDateTimeValidator")

        # Add basic type validator if no format validator
        elif field_type in self.TYPE_VALIDATORS and field_type not in [
            "array"
        ]:
            validators.append(self.TYPE_VALIDATORS[field_type])
            validator_name = self.TYPE_VALIDATORS[field_type].split("(")[0]
            self.import_validators.add(validator_name)

        # Handle numeric ranges
        if field_type in ("integer", "number"):
            minimum = spec.get("minimum")
            maximum = spec.get("maximum")
            if minimum is not None or maximum is not None:
                args = []
                if minimum is not None:
                    args.append(f"min_value={minimum}")
                if maximum is not None:
                    args.append(f"max_value={maximum}")
                validators.append(f"RangeValidator({', '.join(args)})")
                self.import_validators.add("RangeValidator")

        # Handle string constraints
        if field_type == "string":
            min_length = spec.get("minLength")
            max_length = spec.get("maxLength")
            if min_length is not None or max_length is not None:
                args = []
                if min_length is not None:
                    args.append(f"min_length={min_length}")
                if max_length is not None:
                    args.append(f"max_length={max_length}")
                validators.append(f"LengthValidator({', '.join(args)})")
                self.import_validators.add("LengthValidator")

        # Handle pattern validation
        pattern = spec.get("pattern")
        if pattern:
            validators.append(
                f"RegexValidator(r'{pattern}', 'Pattern validation failed.')"
            )
            self.import_validators.add("RegexValidator")

        # Handle enum validation
        enum_values = spec.get("enum")
        if enum_values:
            validators.append(f"InArrayValidator({json.dumps(enum_values)})")
            self.import_validators.add("InArrayValidator")

        # Handle arrays
        if field_type == "array":
            validators.append("IsArrayValidator()")
            self.import_validators.add("IsArrayValidator")

            # Add array length validation if specified
            min_items = spec.get("minItems")
            max_items = spec.get("maxItems")
            if min_items is not None or max_items is not None:
                args = []
                if min_items is not None:
                    args.append(f"min_length={min_items}")
                if max_items is not None:
                    args.append(f"max_length={max_items}")
                validators.append(f"ArrayLengthValidator({', '.join(args)})")
                self.import_validators.add("ArrayLengthValidator")

        return {
            "attr": attr,
            "type": field_type,
            "required": attr in required_fields,
            "default": spec.get("default"),
            "description": spec.get("description", ""),
            "filters": filters,
            "validators": validators,
        }

    def get_global_validators(self, schema: Dict[str, Any]) -> List[str]:
        """Get global validators based on schema properties."""
        global_validators = []

        if schema.get("additionalProperties") is False:
            gv = "CustomJsonValidator({'additionalProperties': False})"
            global_validators.append(gv)
            self.import_validators.add("CustomJsonValidator")

        return global_validators

    def get_imports(self) -> dict:
        """Get all required imports based on used components."""
        return {
            "filters": sorted(self.import_filters),
            "validators": sorted(self.import_validators),
            "enums": sorted(self.import_enums),
        }

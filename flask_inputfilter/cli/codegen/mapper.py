from __future__ import annotations

import json
from typing import Any, Dict, List, Set


class TypeMapper:
    """Enhanced mapping from JSON Schema types to Flask InputFilter
    components."""

    MAPPING = {
        "string": {
            "filter": "StringTrimFilter",
            "validator": "IsStringValidator",
            "format": {
                "email": ["RegexValidator", "RegexEnum.EMAIL.value"],
                "uri": ["RegexValidator", "RegexEnum.URL.value"],
                "uuid": ["IsUUIDValidator"],
                "date": ["IsDateValidator"],
                "date-time": ["IsDateTimeValidator"],
                "ipv4": ["RegexValidator", "RegexEnum.IPV4.value"],
                "ipv6": ["RegexValidator", "RegexEnum.IPV6.value"],
                "enum": ["InArrayValidator"],
            }
        },
        "integer": {
            "validator": "IsIntegerValidator"
        },
        "number": {
            "validator": "IsFloatValidator"
        },
        "boolean": {
            "validator": "IsBooleanValidator"
        },
        "array": {
            "validator": "IsArrayValidator"
        },
    }

    def __init__(self) -> None:
        self.import_filters: Set[str] = set()
        self.import_validators: Set[str] = set()
        self.import_enums: Set[str] = set()

    def map_field(
        self, attr: str, spec: Dict[str, Any]
    ) -> dict:
        """Map a single field from JSON schema to InputFilter field
        definition."""
        filters: List[str] = []
        validators: List[str] = []

        field_type = spec.get("type")
        field_format = spec.get("format")
        error_msg = spec.get("error")



        return {
            "attr": attr,
            "type": field_type,
            "required": spec.get("required"),
            "default": spec.get("default"),
            "description": spec.get("description", ""),
            "filters": filters,
            "validators": validators,
        }

    def get_imports(self) -> dict:
        """Get all required imports based on used components."""
        return {
            "filters": sorted(self.import_filters),
            "validators": sorted(self.import_validators),
            "enums": sorted(self.import_enums),
        }

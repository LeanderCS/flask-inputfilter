from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from flask_inputfilter.enums import RegexEnum


@dataclass(frozen=True)
class TypeMapping:
    """
    Bidirectional mapping between an OpenAPI type/format pair and the
    InputFilter components that represent it.

    Class names are stored as strings so that code generation never has to
    import the actual filter or validator classes.
    """

    openapi_type: str
    openapi_format: Optional[str]
    filter_name: Optional[str]
    validator_name: Optional[str]
    python_type: Optional[str]


TYPE_MAPPINGS: list[TypeMapping] = [
    TypeMapping("string", None, None, "IsStringValidator", "str"),
    TypeMapping(
        "integer", None, "ToIntegerFilter", "IsIntegerValidator", "int"
    ),
    TypeMapping("number", None, "ToFloatFilter", "IsFloatValidator", "float"),
    TypeMapping(
        "boolean", None, "ToBooleanFilter", "IsBooleanValidator", "bool"
    ),
    TypeMapping("array", None, None, "IsArrayValidator", "list"),
    TypeMapping("string", "date", "ToDateFilter", "IsDateValidator", None),
    TypeMapping(
        "string", "date-time", "ToDateTimeFilter", "IsDateTimeValidator", None
    ),
    TypeMapping("string", "uuid", None, "IsUUIDValidator", None),
    TypeMapping("string", "uri", None, "IsUrlValidator", None),
    TypeMapping("string", "email", None, "IsEmailValidator", None),
]


@dataclass(frozen=True)
class ConstraintMapping:
    """Mapping between a validator's constructor parameters (also available as
    instance attributes via ``__slots__``) and the OpenAPI schema keywords they
    correspond to."""

    validator_name: str
    params_to_keywords: dict[str, str]


CONSTRAINT_MAPPINGS: list[ConstraintMapping] = [
    ConstraintMapping(
        "LengthValidator",
        {"min_length": "minLength", "max_length": "maxLength"},
    ),
    ConstraintMapping(
        "ArrayLengthValidator",
        {"min_length": "minItems", "max_length": "maxItems"},
    ),
    ConstraintMapping(
        "RangeValidator",
        {"min_value": "minimum", "max_value": "maximum"},
    ),
    ConstraintMapping("RegexValidator", {"pattern": "pattern"}),
    ConstraintMapping("InArrayValidator", {"haystack": "enum"}),
]

# Well-known regex patterns that translate to an OpenAPI ``format``
# instead of a raw ``pattern`` keyword.
PATTERN_TO_FORMAT: dict[str, str] = {
    RegexEnum.EMAIL.value: "email",
    RegexEnum.URL.value: "uri",
    RegexEnum.UUID.value: "uuid",
    RegexEnum.ISO_DATE.value: "date",
    RegexEnum.ISO_DATETIME.value: "date-time",
}


def type_mapping_for(
    openapi_type: Optional[str], openapi_format: Optional[str] = None
) -> Optional[TypeMapping]:
    """
    Look up the mapping for an OpenAPI type/format pair.

    Falls back to the format-less mapping of the type if the exact format is
    unknown.
    """
    if openapi_format is not None:
        for mapping in TYPE_MAPPINGS:
            if (
                mapping.openapi_type == openapi_type
                and mapping.openapi_format == openapi_format
            ):
                return mapping

    for mapping in TYPE_MAPPINGS:
        if (
            mapping.openapi_type == openapi_type
            and mapping.openapi_format is None
        ):
            return mapping

    return None


def type_mapping_for_component(
    component_name: str,
) -> Optional[TypeMapping]:
    """Look up the mapping for a filter or validator class name."""
    for mapping in TYPE_MAPPINGS:
        if component_name in (mapping.filter_name, mapping.validator_name):
            return mapping

    return None


def constraint_mapping_for(
    validator_name: str,
) -> Optional[ConstraintMapping]:
    """Look up the constraint mapping for a validator class name."""
    for mapping in CONSTRAINT_MAPPINGS:
        if mapping.validator_name == validator_name:
            return mapping

    return None

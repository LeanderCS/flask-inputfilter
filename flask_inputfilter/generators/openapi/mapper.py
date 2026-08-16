from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.enums import RegexEnum

from .mapping_registry import TypeMapping, type_mapping_for


class SchemaMapper:
    """Maps OpenAPI schema definitions to InputFilter field configurations."""

    @staticmethod
    def map_field(
        property_name: str,
        property_schema: dict[str, Any],
        required_fields: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """
        Map an OpenAPI property schema to InputFilter field configuration.

        Args:
            property_name: Name of the property.
            property_schema: OpenAPI property schema definition.
            required_fields: List of required field names.

        Returns:
            Dictionary with field configuration.
        """
        if required_fields is None:
            required_fields = []

        is_required = property_name in required_fields
        field_config: dict[str, Any] = {
            "required": is_required,
            "filters": [],
            "validators": [],
        }

        # Handle default value
        if "default" in property_schema:
            field_config["default"] = property_schema["default"]

        # Handle $ref references
        if "$ref" in property_schema:
            # This will be handled by the code generator
            field_config["_ref"] = property_schema["$ref"]
            return field_config

        # Handle nested objects
        if property_schema.get("type") == "object":
            nested_class_name = SchemaMapper._generate_nested_class_name(
                property_name
            )
            field_config["_nested"] = True
            field_config["_nested_class_name"] = nested_class_name
            field_config["_nested_schema"] = property_schema
            return field_config

        # Handle arrays
        if property_schema.get("type") == "array":
            return SchemaMapper._map_array_field(
                property_name, property_schema, field_config
            )

        # Map basic types
        schema_type = property_schema.get("type")
        format_type = property_schema.get("format")

        if schema_type == "string":
            SchemaMapper._map_string_field(
                property_schema, format_type, field_config
            )
        elif schema_type in ("integer", "number"):
            SchemaMapper._map_numeric_field(
                schema_type, property_schema, field_config
            )
        elif schema_type == "boolean":
            SchemaMapper._apply_type_mapping(
                type_mapping_for("boolean"), field_config
            )

        # Handle enum
        if "enum" in property_schema:
            field_config["validators"].append(
                {
                    "type": "InArrayValidator",
                    "haystack": property_schema["enum"],
                }
            )

        return field_config

    @staticmethod
    def _apply_type_mapping(
        mapping: Optional[TypeMapping], field_config: dict[str, Any]
    ) -> None:
        """Append the filter and validator of a type mapping."""

        if mapping is None:
            return

        if mapping.filter_name:
            field_config["filters"].append({"type": mapping.filter_name})
        if mapping.validator_name:
            field_config["validators"].append({"type": mapping.validator_name})

    @staticmethod
    def _map_string_field(
        property_schema: dict[str, Any],
        format_type: Optional[str],
        field_config: dict[str, Any],
    ) -> None:
        """Map string type field."""

        format_mapping = None
        if format_type is not None and format_type != "email":
            format_mapping = type_mapping_for("string", format_type)
            if format_mapping and not format_mapping.openapi_format:
                format_mapping = None  # unknown format, fell back to base

        # IsStringValidator only applies when no format-specific filter
        # (e.g. ToDateFilter) converts the value away from str before
        # validators run.
        if not (format_mapping and format_mapping.filter_name):
            SchemaMapper._apply_type_mapping(
                type_mapping_for("string"), field_config
            )

        # Handle format
        if format_type == "email":
            field_config["validators"].append(
                {
                    "type": "RegexValidator",
                    "pattern": RegexEnum.EMAIL.value,
                }
            )
        elif format_mapping is not None:
            SchemaMapper._apply_type_mapping(format_mapping, field_config)

        # Handle pattern
        if "pattern" in property_schema:
            field_config["validators"].append(
                {
                    "type": "RegexValidator",
                    "pattern": property_schema["pattern"],
                }
            )

        # Handle minLength/maxLength
        if "minLength" in property_schema or "maxLength" in property_schema:
            field_config["validators"].append(
                {
                    "type": "LengthValidator",
                    "min_length": property_schema.get("minLength"),
                    "max_length": property_schema.get("maxLength"),
                }
            )

    @staticmethod
    def _map_numeric_field(
        schema_type: str,
        property_schema: dict[str, Any],
        field_config: dict[str, Any],
    ) -> None:
        """Map integer or number type field."""

        SchemaMapper._apply_type_mapping(
            type_mapping_for(schema_type), field_config
        )

        # Handle minimum/maximum
        if "minimum" in property_schema or "maximum" in property_schema:
            field_config["validators"].append(
                {
                    "type": "RangeValidator",
                    "min_value": property_schema.get("minimum"),
                    "max_value": property_schema.get("maximum"),
                }
            )

    @staticmethod
    def _map_array_field(
        property_name: str,
        property_schema: dict[str, Any],
        field_config: dict[str, Any],
    ) -> dict[str, Any]:
        """Map array type field."""

        field_config["validators"].append({"type": "IsArrayValidator"})

        items_schema = property_schema.get("items", {})

        # Handle array of objects
        if items_schema.get("type") == "object" or "$ref" in items_schema:
            nested_class_name = SchemaMapper._generate_nested_class_name(
                property_name, suffix="Item"
            )
            field_config["_array_nested"] = True
            field_config["_array_nested_class_name"] = nested_class_name
            field_config["_array_nested_schema"] = items_schema
        else:
            element_validators = []

            items_type = items_schema.get("type")
            items_format = items_schema.get("format")

            if items_type == "string":
                element_validators.append({"type": "IsStringValidator"})

                if items_format == "email":
                    element_validators.append(
                        {
                            "type": "RegexValidator",
                            "pattern": RegexEnum.EMAIL.value,
                        }
                    )

            elif items_type == "integer":
                element_validators.append({"type": "IsIntegerValidator"})

            elif items_type == "number":
                element_validators.append({"type": "IsFloatValidator"})

            if element_validators:
                field_config["validators"].append(
                    {
                        "type": "ArrayElementValidator",
                        "element_filter": element_validators,
                    }
                )

        if "minItems" in property_schema or "maxItems" in property_schema:
            field_config["validators"].append(
                {
                    "type": "ArrayLengthValidator",
                    "min_length": property_schema.get("minItems"),
                    "max_length": property_schema.get("maxItems"),
                }
            )

        return field_config

    @staticmethod
    def _generate_nested_class_name(
        property_name: str, suffix: str = ""
    ) -> str:
        """
        Generate a class name for nested schema.

        Args:
            property_name: Name of the property.
            suffix: Optional suffix to add.

        Returns:
            Generated class name.
        """
        parts = property_name.replace("-", "_").split("_")
        pascal_name = "".join(word.capitalize() for word in parts)

        return f"{pascal_name}{suffix}InputFilter"

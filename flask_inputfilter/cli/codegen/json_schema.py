from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Union

import jsonschema

from .mapper import TypeMapper
from .renderer import TemplateRenderer


class JsonSchemaCodegen:
    """JSON Schema to InputFilter code generator using jsonschema library."""

    @staticmethod
    def validate_schema(schema: Dict[str, Any]) -> None:
        """Validate the JSON schema using jsonschema library."""
        try:
            jsonschema.Draft202012Validator.check_schema(schema) # was zur hölle ist Draft202012Validator nutzte da einen richtigen
        except jsonschema.SchemaError as e:
            raise ValueError(f"Invalid JSON Schema: {e}")

    @staticmethod
    def build_context(
        schema: Dict[str, Any],
        class_name: str,
        strict: bool = False,
    ) -> Dict[str, Any]:
        """Build template context from JSON schema."""
        mapper = TypeMapper()

        if strict:
            JsonSchemaCodegen.validate_schema(schema)

        properties: Dict[str, Any] = schema.get("properties", {})

        if not properties and strict:
            raise ValueError(
                "No properties found in schema and strict mode is enabled"
            )

        fields = []
        for name, spec in properties.items():
            field_def = mapper.map_field(name, spec)
            fields.append(field_def)

        imports = mapper.get_imports()

        return {
            "class_name": class_name,
            "schema_title": schema.get("title", ""),
            "schema_description": schema.get("description", ""),
            "import_filters": imports["filters"],
            "import_validators": imports["validators"],
            "import_enums": imports["enums"],
            "fields": fields,
        }

    @staticmethod
    def generate_from_schema(
        schema: Dict[str, Any],
        class_name: str,
        template_path: str,
        **kwargs,
    ) -> str:
        """Generate InputFilter code from JSON schema."""
        context = JsonSchemaCodegen.build_context(schema, class_name, **kwargs)
        return TemplateRenderer().render_inputfilter(template_path, context)

    @staticmethod
    def generate_from_file(
        schema_path: Union[str, Path],
        class_name: str,
        template_path: str,
        **kwargs,
    ) -> str:
        """Generate InputFilter code from JSON schema file."""
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        return JsonSchemaCodegen.generate_from_schema(
            schema, class_name, template_path, **kwargs
        )

from __future__ import annotations

import keyword
from typing import TYPE_CHECKING, Any, Optional, Tuple

from flask_inputfilter.generators.openapi.mapper import SchemaMapper
from flask_inputfilter.generators.openapi.naming import (
    to_input_filter_class_name,
)
from flask_inputfilter.generators.openapi.validator_formatter import (
    ValidatorFormatter,
)

if TYPE_CHECKING:
    from flask_inputfilter.generators.openapi.parser import OpenAPIParser

NestedClass = Tuple[str, str]


class CodeGenerator:
    """Generates Python code for InputFilter classes from OpenAPI schemas."""

    def __init__(self, parser: Optional[OpenAPIParser] = None) -> None:
        self.parser = parser
        self.generated_classes: dict[str, str] = {}
        self.used_filters: set[str] = set()
        self.used_validators: set[str] = set()
        self._schemas_cache: Optional[dict[str, Any]] = None

    def generate_class(
        self,
        schema_name: str,
        schema: dict[str, Any],
        parser: Optional[OpenAPIParser] = None,
        include_imports: bool = False,
        class_name: Optional[str] = None,
    ) -> str:
        """
        Generate Python code for an InputFilter class from a schema.

        Args:
            schema_name: Name of the schema.
            schema: Schema definition.
            parser: OpenAPI parser for resolving references.
            include_imports: Whether to include import statements.
            class_name: Canonical class name. When set, used as-is instead
                of deriving a name from ``schema_name``.

        Returns:
            Python code as string (class definition only if
            include_imports=False).
        """
        if parser is not None and parser is not self.parser:
            self.parser = parser
            self._schemas_cache = None

        resolved_name = class_name or self.to_class_name(schema_name)
        required_fields = schema.get("required", [])
        properties = self._prepare_properties(schema.get("properties", {}))

        nested_classes: list[NestedClass] = []
        field_definitions: list[str] = []
        processed_nested: set[str] = set()

        for prop_name, prop_schema in properties.items():
            self.handle_field_config(
                prop_name,
                prop_schema,
                required_fields,
                processed_nested,
                nested_classes,
                field_definitions,
            )

        class_code = self.generate_class_code(
            resolved_name,
            field_definitions,
            self.filter_nested_classes(nested_classes),
        )

        if include_imports:
            return self.generate_imports() + "\n\n" + class_code

        return class_code

    def generate_imports(self) -> str:
        result = [
            "from __future__ import annotations",
            "",
            "from typing import Any",
            "from flask_inputfilter import InputFilter",
            "from flask_inputfilter.declarative import field",
        ]

        if self.used_filters:
            result.append(
                "from flask_inputfilter.filters import "
                + ", ".join(sorted(self.used_filters))
            )

        if self.used_validators:
            if len(self.used_validators) == 1:
                only_validator = next(iter(self.used_validators))
                result.append(
                    "from flask_inputfilter.validators import "
                    f"{only_validator}"
                )
            else:
                result.append(
                    "from flask_inputfilter.validators import (\n"
                    + ",\n".join(
                        f"    {v}" for v in sorted(self.used_validators)
                    )
                    + ",\n)"
                )

        return "\n".join(result)

    def handle_field_config(
        self,
        prop_name: str,
        prop_schema: dict[str, Any],
        required_fields: list[str],
        processed_nested: set[str],
        nested_classes: list[NestedClass],
        field_definitions: list[str],
    ) -> None:
        warning = self._property_name_warning(prop_name)
        if warning is not None:
            field_definitions.append(warning)
            return

        field_config = SchemaMapper.map_field(
            prop_name, prop_schema, required_fields
        )

        nested_class_name, schema_to_generate = self._resolve_nested_target(
            field_config
        )
        if nested_class_name and schema_to_generate is not None:
            self._generate_nested_class_if_needed(
                nested_class_name,
                schema_to_generate,
                processed_nested,
                nested_classes,
            )

        if field_config.get("_array_nested") and nested_class_name:
            self._attach_array_element_filter(field_config, nested_class_name)

        self._track_field_components(field_config)

        field_input_filter = (
            None if field_config.get("_array_nested") else nested_class_name
        )
        field_definitions.append(
            self._generate_field_definition(
                prop_name, field_config, field_input_filter
            )
        )

    def filter_nested_classes(
        self, nested_classes: list[NestedClass]
    ) -> list[str]:
        top_level_class_names = {
            self.to_class_name(schema_name)
            for schema_name in self._top_level_schemas()
        }
        return [
            code
            for class_name, code in nested_classes
            if class_name not in top_level_class_names
        ]

    @staticmethod
    def generate_class_code(
        class_name: str,
        field_definitions: list[str],
        nested_classes: list[str],
        base_class: str = "InputFilter",
    ) -> str:
        lines = []

        for nested_class in nested_classes:
            lines.append(nested_class)
            lines.append("")

        lines.append(f"class {class_name}({base_class}):")
        has_statements = any(
            not definition.lstrip().startswith("#")
            for definition in field_definitions
        )
        if not has_statements:
            lines.append("    pass")
        for i, field_def in enumerate(field_definitions):
            if i > 0 or not has_statements:
                lines.append("")
            lines.extend(
                "    " + line
                for line in field_def.split("\n")
                if line.strip()
            )

        return "\n".join(lines)

    @staticmethod
    def to_class_name(name: str) -> str:
        return to_input_filter_class_name(name)

    def _prepare_properties(
        self, properties: dict[str, Any]
    ) -> dict[str, Any]:
        prepared: dict[str, Any] = {}
        for prop_name, prop_schema in properties.items():
            if not isinstance(prop_schema, dict):
                prepared[prop_name] = prop_schema
                continue
            if "$ref" in prop_schema:
                prepared[prop_name] = prop_schema
            elif self.parser:
                prepared[prop_name] = self.parser.resolve_schema_refs(
                    prop_schema
                )
            else:
                prepared[prop_name] = prop_schema
        return prepared

    def _top_level_schemas(self) -> dict[str, Any]:
        if self.parser is None:
            return {}
        if self._schemas_cache is None:
            self._schemas_cache = self.parser.extract_schemas()
        return self._schemas_cache

    def _is_top_level_schema(self, schema_name: str) -> bool:
        return schema_name in self._top_level_schemas()

    @staticmethod
    def _property_name_warning(prop_name: str) -> Optional[str]:
        if prop_name.isidentifier() and not keyword.iskeyword(prop_name):
            return None
        return (
            f"# WARNING: property {prop_name!r} is not a valid Python "
            f"identifier and was skipped."
        )

    def _resolve_nested_target(
        self, field_config: dict[str, Any]
    ) -> tuple[Optional[str], Optional[dict[str, Any]]]:
        """
        Resolve nested class name and optional schema to generate.

        Returns:
            ``(class_name, schema)`` when a nested class must be emitted,
            ``(class_name, None)`` for top-level ``$ref`` targets that are
            only referenced, or ``(None, None)`` for plain fields.
        """
        if field_config.get("_nested"):
            return (
                field_config["_nested_class_name"],
                field_config["_nested_schema"],
            )

        if field_config.get("_array_nested"):
            return self._resolve_array_nested_target(field_config)

        ref = field_config.get("_ref")
        if not ref or not self.parser:
            return None, None

        ref_schema = self.parser.resolve_ref(ref)
        if not ref_schema:
            return None, None

        ref_name = ref.split("/")[-1]
        ref_class_name = self.to_class_name(ref_name)
        if self._is_top_level_schema(ref_name):
            return ref_class_name, None
        return ref_class_name, ref_schema

    def _resolve_array_nested_target(
        self, field_config: dict[str, Any]
    ) -> tuple[Optional[str], Optional[dict[str, Any]]]:
        nested_schema = field_config["_array_nested_schema"]
        fallback_name = field_config["_array_nested_class_name"]

        if isinstance(nested_schema, dict) and "$ref" in nested_schema:
            if not self.parser:
                return fallback_name, nested_schema

            ref = nested_schema["$ref"]
            ref_schema = self.parser.resolve_ref(ref)
            ref_name = ref.split("/")[-1]
            ref_class_name = self.to_class_name(ref_name)
            if self._is_top_level_schema(ref_name):
                return ref_class_name, None
            return ref_class_name, ref_schema or nested_schema

        return fallback_name, nested_schema

    @staticmethod
    def _attach_array_element_filter(
        field_config: dict[str, Any], nested_class_name: str
    ) -> None:
        field_config["validators"].append(
            {
                "type": "ArrayElementValidator",
                "element_filter": nested_class_name,
            }
        )

    def _track_field_components(self, field_config: dict[str, Any]) -> None:
        for filter_config in field_config.get("filters", []):
            if isinstance(filter_config, dict):
                filter_type = filter_config.get("type")
                if filter_type:
                    self.used_filters.add(filter_type)

        for validator_config in field_config.get("validators", []):
            if isinstance(validator_config, dict):
                validator_type = validator_config.get("type")
                if validator_type:
                    self.used_validators.add(validator_type)
                    if validator_type == "ArrayElementValidator":
                        self._track_array_element_validators(validator_config)

    def _track_array_element_validators(
        self, validator_config: dict[str, Any]
    ) -> None:
        element_filter = validator_config.get("element_filter", [])
        if isinstance(element_filter, str):
            return
        if not isinstance(element_filter, list):
            return
        for elem_val in element_filter:
            if isinstance(elem_val, dict):
                elem_type = elem_val.get("type")
                if elem_type:
                    self.used_validators.add(elem_type)

    def _generate_nested_class_if_needed(
        self,
        nested_class_name: str,
        nested_schema: dict[str, Any],
        processed_nested: set[str],
        nested_classes: list[NestedClass],
    ) -> None:
        if nested_class_name in self.generated_classes:
            return

        schema_for_generation = nested_schema
        if (
            self.parser
            and isinstance(nested_schema, dict)
            and "$ref" not in nested_schema
        ):
            schema_for_generation = self.parser.resolve_schema_refs(
                nested_schema
            )

        nested_code = self.generate_class(
            nested_class_name,
            schema_for_generation,
            self.parser,
            include_imports=False,
            class_name=nested_class_name,
        )
        if nested_class_name not in processed_nested:
            nested_classes.append((nested_class_name, nested_code))
            processed_nested.add(nested_class_name)
        self.generated_classes[nested_class_name] = nested_code

    @staticmethod
    def _infer_type_hint(
        field_config: dict[str, Any], nested_class_name: Optional[str] = None
    ) -> str:
        if nested_class_name:
            return "dict"
        if field_config.get("_array_nested"):
            return "list[dict]"

        validator_to_type = {
            "IsIntegerValidator": "int",
            "IsFloatValidator": "float",
            "IsBooleanValidator": "bool",
            "IsStringValidator": "str",
        }
        for validator in field_config.get("validators", []):
            if isinstance(validator, dict):
                validator_type = validator.get("type")
                if validator_type in validator_to_type:
                    return validator_to_type[validator_type]

        return "Any"

    @staticmethod
    def _build_field_params(
        field_config: dict[str, Any], nested_class_name: Optional[str] = None
    ) -> list[str]:
        params = []

        if field_config.get("required"):
            params.append("required=True")
        elif "default" in field_config:
            default_val = field_config["default"]
            if isinstance(default_val, str):
                params.append(f"default={default_val!r}")
            else:
                params.append(f"default={default_val}")

        if nested_class_name:
            params.append(f"input_filter={nested_class_name}")

        filters = [
            f"{filter_config.get('type')}()"
            for filter_config in field_config.get("filters", [])
            if isinstance(filter_config, dict) and filter_config.get("type")
        ]
        if filters:
            params.append(f"filters=[{', '.join(filters)}]")

        validators = []
        for validator_config in field_config.get("validators", []):
            if isinstance(validator_config, dict):
                formatted = ValidatorFormatter.format(validator_config)
                if formatted:
                    validators.append(formatted)

        if validators:
            if len(validators) == 1:
                params.append(f"validators=[{validators[0]}]")
            else:
                validator_lines = ["validators=["]
                validator_lines.extend(
                    f"        {validator}," for validator in validators
                )
                validator_lines.append("    ]")
                params.append("\n".join(validator_lines))

        return params

    @staticmethod
    def _format_field_params(params: list[str]) -> list[str]:
        if not params:
            return [")"]
        if len(params) == 1:
            return [f"    {params[0]},", ")"]
        lines = [f"    {param}," for param in params]
        lines.append(")")
        return lines

    @staticmethod
    def _generate_field_definition(
        prop_name: str,
        field_config: dict[str, Any],
        nested_class_name: Optional[str] = None,
    ) -> str:
        type_hint = CodeGenerator._infer_type_hint(
            field_config, nested_class_name
        )
        params = CodeGenerator._build_field_params(
            field_config, nested_class_name
        )
        param_lines = CodeGenerator._format_field_params(params)

        lines = [f"{prop_name}: {type_hint} = field("]
        lines.extend(param_lines)

        return "\n".join(lines)

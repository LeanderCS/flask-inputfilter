from __future__ import annotations

import datetime
from enum import Enum
from typing import Any, Optional, Union

from flask_inputfilter.models import BaseFilter, BaseValidator

from .mapping_registry import (
    PATTERN_TO_FORMAT,
    constraint_mapping_for,
    type_mapping_for_component,
)

ANNOTATION_TO_TYPE = {
    "str": "string",
    "int": "integer",
    "float": "number",
    "bool": "boolean",
    "list": "array",
    "dict": "object",
}


class SchemaExporter:
    """
    Exports InputFilter classes to OpenAPI 3.0 schema objects.

    Everything that has no clean OpenAPI representation (custom
    validators, computed fields, conditions, ...) degrades gracefully
    into ``x-`` extension keywords instead of raising, so the output is
    always a valid schema object.
    """

    def __init__(
        self,
        inline_nested: bool = False,
        include_extensions: bool = True,
        include_computed: bool = False,
    ) -> None:
        """
        Args:
            inline_nested: Embed nested InputFilters as inline object
                schemas instead of ``$ref`` references (always the case
                in :meth:`export`, which has no components container).
            include_extensions: Emit ``x-`` extension keywords for
                features without an OpenAPI equivalent.
            include_computed: Include computed fields (excluded by
                default since they are outputs, not request inputs).
        """
        self.inline_nested = inline_nested
        self.include_extensions = include_extensions
        self.include_computed = include_computed

    def export(self, input_filter: Any) -> dict[str, Any]:
        """
        Export a single InputFilter to a bare OpenAPI schema object.

        Nested InputFilters are always inlined since there is no
        components container to reference into.

        Args:
            input_filter: InputFilter class or instance.

        Returns:
            OpenAPI schema object as dictionary.
        """
        return self._export_schema(
            input_filter, components=None, visiting=frozenset()
        )

    def export_components(self, *input_filters: Any) -> dict[str, Any]:
        """
        Export InputFilters to a ``components/schemas`` document.

        Nested InputFilters are collected transitively and referenced
        via ``$ref`` (unless ``inline_nested`` is set).

        Args:
            *input_filters: InputFilter classes or instances.

        Returns:
            ``{"components": {"schemas": {...}}}`` dictionary.
        """
        components: dict[str, Any] = {}

        for input_filter in input_filters:
            name = self._component_name(input_filter)
            if name not in components:
                components[name] = None  # cycle guard
                components[name] = self._export_schema(
                    input_filter, components, visiting=frozenset()
                )

        return {"components": {"schemas": components}}

    def _export_schema(
        self,
        input_filter: Any,
        components: Optional[dict[str, Any]],
        visiting: frozenset = frozenset(),
    ) -> dict[str, Any]:
        klass = (
            input_filter
            if isinstance(input_filter, type)
            else type(input_filter)
        )
        if klass in visiting:
            # Circular reference while inlining: emit a plain object
            # instead of recursing forever.
            node: dict[str, Any] = {"type": "object"}
            if self.include_extensions:
                node["x-circular-ref"] = self._component_name(klass)
            return node
        visiting = visiting | {klass}

        instance = (
            input_filter() if isinstance(input_filter, type) else input_filter
        )

        annotations = self._collect_annotations(type(instance))

        properties: dict[str, Any] = {}
        required: list[str] = []

        for field_name, field_info in instance.fields.items():
            if field_info.computed and not self.include_computed:
                continue

            property_schema = self._export_field(
                field_name, field_info, annotations, components, visiting
            )
            properties[field_name] = property_schema

            if field_info.required:
                required.append(field_name)

        schema: dict[str, Any] = {"type": "object"}
        if properties:
            schema["properties"] = properties
        if required:
            schema["required"] = required

        if self.include_extensions:
            conditions = [
                self._describe_condition(condition)
                for condition in instance.conditions
            ]
            if conditions:
                schema["x-conditions"] = conditions

            global_validators = [
                type(validator).__name__
                for validator in instance.global_validators
            ]
            if global_validators:
                schema["x-global-validators"] = global_validators

        return schema

    def _export_field(
        self,
        field_name: str,
        field_info: Any,
        annotations: dict[str, Any],
        components: Optional[dict[str, Any]],
        visiting: frozenset = frozenset(),
    ) -> dict[str, Any]:
        # Nested InputFilter fields become object schemas or $refs.
        if field_info.input_filter is not None:
            property_schema = self._nested_schema(
                field_info.input_filter, components, visiting
            )
        else:
            filters, validators = self._classify_components(field_info)
            property_schema = self._schema_from_components(
                filters, validators, components, visiting
            )

            if "type" not in property_schema:
                annotated = self._type_from_annotation(
                    annotations.get(field_name)
                )
                if annotated:
                    property_schema = {"type": annotated, **property_schema}

        if field_info.default is not None:
            default = self._serialize_default(field_info.default)
            if default is not None:
                property_schema["default"] = default

        if self.include_extensions:
            if field_info.computed:
                property_schema["x-computed"] = True
            if field_info.copy:
                property_schema["x-copied-from"] = field_info.copy
            if field_info.external_api:
                property_schema["x-external-api"] = True
            if field_info.fallback is not None:
                fallback = self._serialize_default(field_info.fallback)
                if fallback is not None:
                    property_schema["x-fallback"] = fallback

        return property_schema

    def _schema_from_components(
        self,
        filters: list[BaseFilter],
        validators: list[BaseValidator],
        components: Optional[dict[str, Any]],
        visiting: frozenset = frozenset(),
    ) -> dict[str, Any]:
        schema: dict[str, Any] = {}
        unknown_filters: list[str] = []
        unknown_validators: list[str] = []

        for filter_instance in filters:
            mapping = type_mapping_for_component(
                type(filter_instance).__name__
            )
            if mapping is None:
                unknown_filters.append(type(filter_instance).__name__)
            elif "type" not in schema:
                schema["type"] = mapping.openapi_type
                if mapping.openapi_format:
                    schema["format"] = mapping.openapi_format

        for validator in validators:
            validator_name = type(validator).__name__

            constraint = constraint_mapping_for(validator_name)
            if constraint is not None:
                for param, keyword in constraint.params_to_keywords.items():
                    value = getattr(validator, param, None)
                    if value is not None:
                        schema[keyword] = value

                if validator_name == "RegexValidator":
                    self._apply_pattern_format(schema)
                continue

            if validator_name == "InEnumValidator":
                schema["enum"] = [
                    member.value for member in validator.enum_class
                ]
                continue

            if validator_name == "ArrayElementValidator":
                schema["type"] = "array"
                items = self._items_schema(
                    validator.element_filter, components, visiting
                )
                if items:
                    schema["items"] = items
                continue

            mapping = type_mapping_for_component(validator_name)
            if mapping is None:
                unknown_validators.append(validator_name)
                continue

            if "type" not in schema:
                schema["type"] = mapping.openapi_type
            if mapping.openapi_format and "format" not in schema:
                schema["format"] = mapping.openapi_format

        if self.include_extensions:
            if unknown_filters:
                schema["x-filters"] = unknown_filters
            if unknown_validators:
                schema["x-validators"] = unknown_validators

        return schema

    def _items_schema(
        self,
        element_filter: Union[Any, list],
        components: Optional[dict[str, Any]],
        visiting: frozenset = frozenset(),
    ) -> dict[str, Any]:
        if isinstance(element_filter, BaseValidator):
            element_filter = [element_filter]

        if isinstance(element_filter, list):
            return self._schema_from_components(
                [], element_filter, components, visiting
            )

        # Otherwise it's a nested InputFilter (instance or class).
        return self._nested_schema(element_filter, components, visiting)

    def _nested_schema(
        self,
        input_filter: Any,
        components: Optional[dict[str, Any]],
        visiting: frozenset = frozenset(),
    ) -> dict[str, Any]:
        if components is None or self.inline_nested:
            return self._export_schema(input_filter, components, visiting)

        name = self._component_name(input_filter)
        if name not in components:
            components[name] = None  # cycle guard
            components[name] = self._export_schema(
                input_filter, components, visiting
            )

        return {"$ref": f"#/components/schemas/{name}"}

    @staticmethod
    def _classify_components(
        field_info: Any,
    ) -> tuple[list[BaseFilter], list[BaseValidator]]:
        filters = list(field_info.filters)
        validators = list(field_info.validators)

        for step in field_info.steps:
            if isinstance(step, BaseFilter):
                filters.append(step)
            elif isinstance(step, BaseValidator):
                validators.append(step)

        return filters, validators

    @staticmethod
    def _apply_pattern_format(schema: dict[str, Any]) -> None:
        """Translate well-known regex patterns into an OpenAPI format."""
        pattern = schema.get("pattern")
        format_name = PATTERN_TO_FORMAT.get(pattern)
        if format_name:
            del schema["pattern"]
            schema["format"] = format_name
        if "type" not in schema and pattern is not None:
            schema["type"] = "string"

    @staticmethod
    def _collect_annotations(filter_class: type) -> dict[str, Any]:
        annotations: dict[str, Any] = {}
        for klass in reversed(filter_class.__mro__):
            annotations.update(getattr(klass, "__annotations__", {}))
        return annotations

    @staticmethod
    def _type_from_annotation(annotation: Any) -> Optional[str]:
        if annotation is None:
            return None

        if isinstance(annotation, type):
            name = annotation.__name__
        else:
            name = str(annotation)

        # "list[str]" -> "list", "Optional[int]" -> unsupported.
        name = name.split("[")[0].strip()
        return ANNOTATION_TO_TYPE.get(name)

    @staticmethod
    def _serialize_default(value: Any) -> Any:
        if isinstance(value, (datetime.date, datetime.datetime)):
            return value.isoformat()
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, (list, dict)):
            return value
        return None

    @staticmethod
    def _describe_condition(condition: Any) -> str:
        parts = []
        for slot in getattr(type(condition), "__slots__", ()):
            value = getattr(condition, slot, None)
            if value is not None:
                parts.append(f"{slot}={value!r}")
        arguments = ", ".join(parts)
        return f"{type(condition).__name__}({arguments})"

    @staticmethod
    def _component_name(input_filter: Any) -> str:
        klass = (
            input_filter
            if isinstance(input_filter, type)
            else type(input_filter)
        )
        name = klass.__name__
        if name.endswith("InputFilter") and name != "InputFilter":
            name = name[: -len("InputFilter")]
        return name


def to_openapi_schema(input_filter: Any, **options: Any) -> dict[str, Any]:
    """
    Export an InputFilter class or instance to a bare OpenAPI 3.0 schema
    object.

    Args:
        input_filter: The InputFilter class or instance to export.
        **options: Options forwarded to :class:`SchemaExporter`.

    Returns:
        OpenAPI schema object as dictionary.
    """
    return SchemaExporter(**options).export(input_filter)


def to_openapi_components(
    *input_filters: Any, **options: Any
) -> dict[str, Any]:
    """
    Export InputFilter classes to an OpenAPI ``components/schemas`` document,
    including transitively nested InputFilters.

    Args:
        *input_filters: The InputFilter classes or instances to export.
        **options: Options forwarded to :class:`SchemaExporter`.

    Returns:
        ``{"components": {"schemas": {...}}}`` dictionary.
    """
    return SchemaExporter(**options).export_components(*input_filters)

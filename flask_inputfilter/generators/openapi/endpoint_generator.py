from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from flask_inputfilter.generators.openapi.code_generator import (
    CodeGenerator,
    NestedClass,
)
from flask_inputfilter.generators.openapi.naming import to_pascal_case

if TYPE_CHECKING:
    from flask_inputfilter.generators.openapi.parser import (
        EndpointSpec,
        OpenAPIParser,
    )


class EndpointCodeGenerator:
    """Generates InputFilter classes for OpenAPI endpoints (path/method
    combinations), merging path parameters, query parameters and the JSON
    request body into one filter per endpoint."""

    def __init__(
        self,
        parser: OpenAPIParser,
        code_generator: Optional[CodeGenerator] = None,
    ) -> None:
        self.parser = parser
        self.code_generator = code_generator or CodeGenerator(parser=parser)
        self._used_class_names: set[str] = set()

    def generate_all(
        self, component_class_names: Optional[set[str]] = None
    ) -> list[str]:
        """
        Generate InputFilter classes for all endpoints of the spec.

        Args:
            component_class_names: Class names of already generated
                component schema classes. A request body that is a
                direct ``$ref`` to one of them is expressed as a
                subclass instead of duplicating its fields.

        Returns:
            List of generated class definitions.
        """
        return [
            self.generate_endpoint_class(
                endpoint, component_class_names or set()
            )
            for endpoint in self.parser.extract_endpoints()
        ]

    def generate_endpoint_class(
        self,
        endpoint: EndpointSpec,
        component_class_names: Optional[set[str]] = None,
    ) -> str:
        """
        Generate the InputFilter class for a single endpoint.

        Path parameters are always required (as mandated by OpenAPI),
        query parameters follow their own ``required`` flag and request
        body properties follow the body schema. On a name collision the
        body property wins and a warning comment is emitted.
        """
        component_class_names = component_class_names or set()
        class_name = self.class_name_for(endpoint)
        properties, required, base_class, warnings = (
            self._merge_body_and_parameters(endpoint, component_class_names)
        )

        nested_classes: list[NestedClass] = []
        field_definitions: list[str] = []
        processed_nested: set[str] = set()

        for prop_name, prop_schema in properties.items():
            resolved = (
                prop_schema
                if "$ref" in prop_schema
                else self.parser.resolve_schema_refs(prop_schema)
            )
            self.code_generator.handle_field_config(
                prop_name,
                resolved,
                required,
                processed_nested,
                nested_classes,
                field_definitions,
            )

        class_code = CodeGenerator.generate_class_code(
            class_name,
            field_definitions,
            self.code_generator.filter_nested_classes(nested_classes),
            base_class=base_class,
        )

        if warnings:
            return "\n".join([*warnings, class_code])
        return class_code

    def class_name_for(self, endpoint: EndpointSpec) -> str:
        """
        Determine the class name for an endpoint.

        Uses the PascalCased ``operationId`` if present, otherwise a
        combination of HTTP method and path segments (e.g. ``post`` +
        ``/users/{id}/orders`` becomes ``PostUsersIdOrders``). Name
        collisions get a numeric suffix.
        """
        if endpoint.operation_id:
            base = to_pascal_case(endpoint.operation_id)
        else:
            segments = [
                segment.strip("{}")
                for segment in endpoint.path.split("/")
                if segment
            ]
            base = to_pascal_case("_".join([endpoint.method, *segments]))

        class_name = f"{base}InputFilter"
        suffix = 2
        while class_name in self._used_class_names:
            class_name = f"{base}{suffix}InputFilter"
            suffix += 1

        self._used_class_names.add(class_name)
        return class_name

    def _merge_body_and_parameters(
        self,
        endpoint: EndpointSpec,
        component_class_names: set[str],
    ) -> tuple[dict[str, Any], list[str], str, list[str]]:
        base_class = "InputFilter"
        properties: dict[str, Any] = {}
        required: list[str] = []
        warnings: list[str] = []

        body_schema = endpoint.request_body_schema
        if body_schema:
            ref = body_schema.get("$ref")
            if ref:
                ref_name = ref.split("/")[-1]
                ref_class_name = CodeGenerator.to_class_name(ref_name)
                if ref_class_name in component_class_names:
                    base_class = ref_class_name
                else:
                    body_schema = self.parser.resolve_ref(ref) or {}
                    ref = None
            if not ref:
                properties.update(body_schema.get("properties", {}))
                required.extend(body_schema.get("required", []))

        for parameter in endpoint.parameters:
            name = parameter.get("name")
            if not name:
                continue

            if name in properties:
                warnings.append(
                    f"# WARNING: parameter '{name}' is shadowed by the "
                    f"request body property of the same name."
                )
                continue

            properties[name] = parameter.get("schema", {"type": "string"})
            if parameter.get("in") == "path" or parameter.get("required"):
                required.append(name)

        return properties, required, base_class, warnings

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

SUPPORTED_METHODS = ("get", "post", "put", "patch", "delete")


@dataclass
class EndpointSpec:
    """A single path/method combination of an OpenAPI specification."""

    path: str
    method: str
    operation_id: Optional[str] = None
    request_body_schema: Optional[dict[str, Any]] = None
    parameters: list[dict[str, Any]] = field(default_factory=list)


class OpenAPIParser:
    """Parser for OpenAPI YAML/JSON files."""

    def __init__(
        self, openapi_content: Optional[dict[str, Any]] = None
    ) -> None:
        """
        Initialize the OpenAPI parser.

        Args:
            openapi_content: Pre-parsed OpenAPI content as dict.
        """
        self.openapi_content = openapi_content or {}
        if not isinstance(self.openapi_content, dict):
            raise TypeError(
                "OpenAPI content must be a mapping/dict, got "
                f"{type(self.openapi_content).__name__}"
            )
        self.schemas: dict[str, Any] = {}
        self.refs: dict[str, Any] = {}

    @classmethod
    def from_file(cls, file_path: str | Path) -> OpenAPIParser:
        """
        Create parser from OpenAPI file.

        Args:
            file_path: Path to OpenAPI YAML or JSON file.

        Returns:
            OpenAPIParser instance.

        Raises:
            ImportError: If YAML file provided but pyyaml not installed.
            FileNotFoundError: If file doesn't exist.
            ValueError: If file format is not supported.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"OpenAPI file not found: {file_path}")

        content = path.read_text(encoding="utf-8")

        if path.suffix in (".yaml", ".yml"):
            if not HAS_YAML:
                raise ImportError(
                    "pyyaml is required for YAML files. "
                    "Install it with: pip install pyyaml"
                )
            parsed = yaml.safe_load(content)
        elif path.suffix == ".json":
            parsed = json.loads(content)
        else:
            raise ValueError(
                f"Unsupported file format: {path.suffix}. "
                "Supported formats: .yaml, .yml, .json"
            )

        return cls(openapi_content=parsed)

    @classmethod
    def from_string(cls, content: str, format: str = "yaml") -> OpenAPIParser:
        """
        Create parser from OpenAPI string content.

        Args:
            content: OpenAPI content as string.
            format: Format of content ('yaml' or 'json').

        Returns:
            OpenAPIParser instance.

        Raises:
            ImportError: If YAML format requested but pyyaml not installed.
            ValueError: If format is not supported.
        """
        if format.lower() in ("yaml", "yml"):
            if not HAS_YAML:
                raise ImportError(
                    "pyyaml is required for YAML format. "
                    "Install it with: pip install pyyaml"
                )
            parsed = yaml.safe_load(content)
        elif format.lower() == "json":
            parsed = json.loads(content)
        else:
            raise ValueError(
                f"Unsupported format: {format}. Supported formats: yaml, json"
            )

        return cls(openapi_content=parsed)

    def extract_schemas(self) -> dict[str, Any]:
        """
        Extract all schemas from components/schemas.

        Returns:
            Dictionary mapping schema names to schema definitions.
        """
        if not self.openapi_content:
            return {}

        components = self.openapi_content.get("components", {})
        schemas = components.get("schemas", {})

        self.schemas = schemas
        return schemas

    def get_schema(self, schema_name: str) -> Optional[dict[str, Any]]:
        """
        Get a specific schema by name.

        Args:
            schema_name: Name of the schema to retrieve.

        Returns:
            Schema definition or None if not found.
        """
        if not self.schemas:
            self.extract_schemas()

        return self.schemas.get(schema_name)

    def extract_request_body(
        self, path: str, method: str = "post"
    ) -> Optional[dict[str, Any]]:
        """
        Extract request body schema from a specific path and method.

        Args:
            path: API path (e.g., '/users').
            method: HTTP method (e.g., 'post', 'put').

        Returns:
            Request body schema or None if not found.
        """
        if not self.openapi_content:
            return None

        paths = self.openapi_content.get("paths", {})
        path_spec = paths.get(path)

        if not path_spec:
            return None

        method_spec = path_spec.get(method.lower())

        if not method_spec:
            return None

        request_body = method_spec.get("requestBody")

        if not request_body:
            return None

        content = request_body.get("content", {})
        application_json = content.get("application/json", {})

        return application_json.get("schema")

    def extract_parameters(
        self, path: str, method: str = "get"
    ) -> list[dict[str, Any]]:
        """
        Extract query/path parameters from a specific path and method.

        Args:
            path: API path (e.g., '/users').
            method: HTTP method (e.g., 'get', 'post').

        Returns:
            List of parameter definitions.
        """
        if not self.openapi_content:
            return []

        paths = self.openapi_content.get("paths", {})
        path_spec = paths.get(path)

        if not path_spec:
            return []

        method_spec = path_spec.get(method.lower())

        if not method_spec:
            return []

        parameters = method_spec.get("parameters", [])

        # Also check path-level parameters
        path_parameters = path_spec.get("parameters", [])

        return parameters + path_parameters

    def extract_endpoints(self) -> list[EndpointSpec]:
        """
        Extract all endpoints (path/method combinations) from ``paths``.

        For each endpoint the request body schema (``application/json``,
        unresolved so ``$ref`` stays visible) and the merged
        operation-level and path-level parameters (with parameter-level
        ``$ref`` resolved) are collected.

        Returns:
            List of EndpointSpec instances.
        """
        if not self.openapi_content:
            return []

        endpoints = []

        for path, path_spec in self.openapi_content.get("paths", {}).items():
            if not isinstance(path_spec, dict):
                continue

            for method in SUPPORTED_METHODS:
                method_spec = path_spec.get(method)
                if not isinstance(method_spec, dict):
                    continue

                parameters = []
                for parameter in self.extract_parameters(path, method):
                    if "$ref" in parameter:
                        resolved = self.resolve_ref(parameter["$ref"])
                        if resolved is None:
                            continue
                        parameter = resolved
                    parameters.append(parameter)

                endpoints.append(
                    EndpointSpec(
                        path=path,
                        method=method,
                        operation_id=method_spec.get("operationId"),
                        request_body_schema=self.extract_request_body(
                            path, method
                        ),
                        parameters=parameters,
                    )
                )

        return endpoints

    def resolve_ref(self, ref: str) -> Optional[dict[str, Any]]:
        """
        Resolve a $ref reference.

        Args:
            ref: Reference string (e.g., '#/components/schemas/User').

        Returns:
            Referenced schema or None if not found.
        """
        if not ref.startswith("#/"):
            return None

        parts = ref[2:].split("/")
        current = self.openapi_content

        for part in parts:
            if not isinstance(current, dict):
                return None
            current = current.get(part)
            if current is None:
                return None

        return current

    def resolve_schema_refs(
        self,
        schema: dict[str, Any],
        visited: Optional[set[str]] = None,
    ) -> dict[str, Any]:
        """
        Recursively resolve $ref references in a schema.

        Args:
            schema: Schema definition that may contain $ref.
            visited: Ref paths already being resolved (cycle guard).

        Returns:
            Schema with resolved references. Circular refs become
            ``{"type": "object"}``.
        """
        if not isinstance(schema, dict):
            return schema

        if visited is None:
            visited = set()

        if "$ref" in schema:
            ref = schema["$ref"]
            if ref in visited:
                return {"type": "object"}
            ref_schema = self.resolve_ref(ref)
            if ref_schema:
                return self.resolve_schema_refs(ref_schema, visited | {ref})
            return schema

        resolved = {}

        for key, value in schema.items():
            if isinstance(value, dict):
                resolved[key] = self.resolve_schema_refs(value, visited)
            elif isinstance(value, list):
                resolved[key] = [
                    self.resolve_schema_refs(item, visited)
                    if isinstance(item, dict)
                    else item
                    for item in value
                ]
            else:
                resolved[key] = value

        return resolved

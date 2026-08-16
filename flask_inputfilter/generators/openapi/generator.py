from __future__ import annotations

from pathlib import Path
from typing import Optional

from flask_inputfilter.generators.openapi.code_generator import CodeGenerator
from flask_inputfilter.generators.openapi.endpoint_generator import (
    EndpointCodeGenerator,
)
from flask_inputfilter.generators.openapi.parser import OpenAPIParser


def generate_from_openapi(
    openapi_file: Optional[str | Path] = None,
    openapi_content: Optional[str] = None,
    schema_name: Optional[str] = None,
    output_file: Optional[str | Path] = None,
    format: str = "yaml",
    include_endpoints: bool = False,
    endpoints_only: bool = False,
    path: Optional[str] = None,
    method: Optional[str] = None,
) -> str:
    """
    Generate InputFilter classes from OpenAPI specification.

    Args:
        openapi_file: Path to OpenAPI YAML or JSON file.
        openapi_content: OpenAPI content as string (alternative to file).
        schema_name: Name of specific schema to generate (None for all).
        output_file: Optional path to write generated code to file.
        format: Format of openapi_content ('yaml' or 'json').
        include_endpoints: Also generate one InputFilter per endpoint
            (path/method combination), merging path parameters, query
            parameters and the JSON request body.
        endpoints_only: Generate only endpoint InputFilters, no
            component schema classes.
        path: Restrict endpoint generation to this path.
        method: Restrict endpoint generation to this HTTP method.

    Returns:
        Generated Python code as string.

    Raises:
        ValueError: If neither openapi_file nor openapi_content provided.
        FileNotFoundError: If openapi_file doesn't exist.
    """
    parser = _load_parser(openapi_file, openapi_content, format)
    generate_endpoints = include_endpoints or endpoints_only or path or method
    schemas = parser.extract_schemas()

    if not schemas and not generate_endpoints:
        return "# No schemas found in OpenAPI specification\n"

    code_generator = CodeGenerator(parser=parser)

    if schema_name:
        code = _generate_single_schema(code_generator, schemas, schema_name)
    else:
        class_codes: list[str] = []
        generated_class_names: set[str] = set()

        if not endpoints_only:
            class_codes, generated_class_names = _generate_schema_classes(
                code_generator, schemas
            )

        if generate_endpoints:
            class_codes.extend(
                _generate_endpoint_classes(
                    parser,
                    code_generator,
                    generated_class_names,
                    path=path,
                    method=method,
                )
            )

        if not class_codes:
            return "# No schemas found in OpenAPI specification\n"

        code = "\n\n".join(
            [code_generator.generate_imports(), "", *class_codes]
        )

    if output_file:
        _write_output(output_file, code)

    return code


def _load_parser(
    openapi_file: Optional[str | Path],
    openapi_content: Optional[str],
    format: str,
) -> OpenAPIParser:
    if openapi_file:
        return OpenAPIParser.from_file(openapi_file)
    if openapi_content:
        return OpenAPIParser.from_string(openapi_content, format=format)
    raise ValueError(
        "Either 'openapi_file' or 'openapi_content' must be provided"
    )


def _generate_single_schema(
    code_generator: CodeGenerator,
    schemas: dict,
    schema_name: str,
) -> str:
    schema = schemas.get(schema_name)
    if not schema:
        raise ValueError(f"Schema '{schema_name}' not found in OpenAPI spec")
    return code_generator.generate_class(
        schema_name, schema, include_imports=True
    )


def _generate_schema_classes(
    code_generator: CodeGenerator,
    schemas: dict,
) -> tuple[list[str], set[str]]:
    class_codes: list[str] = []
    generated_class_names: set[str] = set()

    for name, schema in schemas.items():
        class_codes.append(
            code_generator.generate_class(name, schema, include_imports=False)
        )
        generated_class_names.add(code_generator.to_class_name(name))

    return class_codes, generated_class_names


def _generate_endpoint_classes(
    parser: OpenAPIParser,
    code_generator: CodeGenerator,
    generated_class_names: set[str],
    path: Optional[str] = None,
    method: Optional[str] = None,
) -> list[str]:
    endpoint_generator = EndpointCodeGenerator(
        parser=parser, code_generator=code_generator
    )
    endpoints = parser.extract_endpoints()

    if path:
        endpoints = [
            endpoint for endpoint in endpoints if endpoint.path == path
        ]
    if method:
        method_lower = method.lower()
        endpoints = [
            endpoint
            for endpoint in endpoints
            if endpoint.method == method_lower
        ]

    return [
        endpoint_generator.generate_endpoint_class(
            endpoint, generated_class_names
        )
        for endpoint in endpoints
    ]


def _write_output(output_file: str | Path, code: str) -> None:
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding="utf-8")

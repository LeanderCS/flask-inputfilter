from __future__ import annotations

import argparse
import sys
from pathlib import Path

from flask_inputfilter.generators.openapi import generate_from_openapi


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="flask-inputfilter code generator",
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate code from specification",
    )
    generate_subparsers = generate_parser.add_subparsers(
        dest="subcommand", help="Generate from"
    )

    # OpenAPI subcommand
    openapi_parser = generate_subparsers.add_parser(
        "openapi",
        help="Generate from OpenAPI specification",
    )
    openapi_parser.add_argument(
        "openapi_file",
        type=str,
        help="Path to OpenAPI YAML or JSON file",
    )
    openapi_parser.add_argument(
        "--schema",
        type=str,
        help="Generate specific schema only (default: all schemas)",
    )
    openapi_parser.add_argument(
        "--output",
        type=str,
        help="Output file path (single file for all schemas)",
    )
    openapi_parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory path (separate file per schema)",
    )
    openapi_parser.add_argument(
        "--include-endpoints",
        action="store_true",
        help="Also generate one InputFilter per endpoint "
        "(path/method combination)",
    )
    openapi_parser.add_argument(
        "--endpoints-only",
        action="store_true",
        help="Generate only endpoint InputFilters, no schema classes",
    )
    openapi_parser.add_argument(
        "--path",
        type=str,
        help="Restrict endpoint generation to this path (e.g. /users)",
    )
    openapi_parser.add_argument(
        "--method",
        type=str,
        help="Restrict endpoint generation to this HTTP method",
    )

    # Export command
    export_parser = subparsers.add_parser(
        "export",
        help="Export InputFilter classes to a specification",
    )
    export_subparsers = export_parser.add_subparsers(
        dest="subcommand", help="Export to"
    )

    export_openapi_parser = export_subparsers.add_parser(
        "openapi",
        help="Export InputFilters to OpenAPI schemas",
    )
    export_openapi_parser.add_argument(
        "target",
        type=str,
        help="Import target: 'my.module:ClassName' for a single "
        "InputFilter or 'my.module' together with --all",
    )
    export_openapi_parser.add_argument(
        "--all",
        action="store_true",
        help="Export all InputFilter subclasses found in the module",
    )
    export_openapi_parser.add_argument(
        "--components",
        action="store_true",
        help="Wrap the output in a components/schemas document "
        "(implied by --all)",
    )
    export_openapi_parser.add_argument(
        "--format",
        type=str,
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json; yaml requires pyyaml)",
    )
    export_openapi_parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    if args.command == "export" and args.subcommand == "openapi":
        _handle_export(args)
        return

    if args.command != "generate" or args.subcommand != "openapi":
        parser.print_help()
        sys.exit(1)

    # Validate arguments
    if args.output and args.output_dir:
        print(
            "Error: Cannot specify both --output and --output-dir",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.output and not args.output_dir:
        print(
            "Error: Must specify either --output or --output-dir",
            file=sys.stderr,
        )
        sys.exit(1)

    wants_endpoints = (
        args.include_endpoints
        or args.endpoints_only
        or args.path
        or args.method
    )
    if wants_endpoints and args.output_dir:
        print(
            "Error: Endpoint generation is only supported with --output "
            "(single file)",
            file=sys.stderr,
        )
        sys.exit(1)

    openapi_path = Path(args.openapi_file)
    if not openapi_path.exists():
        print(
            f"Error: OpenAPI file not found: {args.openapi_file}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        if args.output_dir:
            # Generate separate files for each schema
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Parse OpenAPI to get all schemas
            from flask_inputfilter.generators.openapi.parser import (
                OpenAPIParser,
            )

            parser = OpenAPIParser.from_file(openapi_path)
            schemas = parser.extract_schemas()

            if not schemas:
                print(
                    "No schemas found in OpenAPI specification",
                    file=sys.stderr,
                )
                sys.exit(1)

            for schema_name in schemas:
                output_file = output_dir / f"{schema_name.lower()}_filter.py"
                generate_from_openapi(
                    openapi_file=openapi_path,
                    schema_name=schema_name,
                    output_file=output_file,
                )
                print(f"Generated: {output_file}")

        else:
            # Generate single file
            output_path = Path(args.output)
            generate_from_openapi(
                openapi_file=openapi_path,
                schema_name=args.schema,
                output_file=output_path,
                include_endpoints=args.include_endpoints,
                endpoints_only=args.endpoints_only,
                path=args.path,
                method=args.method,
            )
            print(f"Generated: {output_path}")

    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _handle_export(args: argparse.Namespace) -> None:
    """Handle the ``export openapi`` subcommand."""
    import importlib
    import inspect
    import json as json_module

    from flask_inputfilter import InputFilter
    from flask_inputfilter.generators.openapi.schema_exporter import (
        to_openapi_components,
        to_openapi_schema,
    )

    module_name, _, class_name = args.target.partition(":")

    if not class_name and not args.all:
        print(
            "Error: Provide 'module:ClassName' or use --all to export "
            "all InputFilters of the module",
            file=sys.stderr,
        )
        sys.exit(1)

    if "" not in sys.path:
        sys.path.insert(0, "")

    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        print(f"Error: Cannot import '{module_name}': {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.all:
            input_filters = [
                obj
                for _, obj in inspect.getmembers(module, inspect.isclass)
                if issubclass(obj, InputFilter)
                and obj is not InputFilter
                and obj.__module__ == module.__name__
            ]
            if not input_filters:
                print(
                    f"Error: No InputFilter subclasses found in "
                    f"'{module_name}'",
                    file=sys.stderr,
                )
                sys.exit(1)
            result = to_openapi_components(*input_filters)
        else:
            input_filter = getattr(module, class_name, None)
            if input_filter is None:
                print(
                    f"Error: '{class_name}' not found in '{module_name}'",
                    file=sys.stderr,
                )
                sys.exit(1)

            if args.components:
                result = to_openapi_components(input_filter)
            else:
                result = to_openapi_schema(input_filter)
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "yaml":
        try:
            import yaml
        except ImportError:
            print(
                "Error: pyyaml is required for YAML output. "
                "Install it with: pip install pyyaml",
                file=sys.stderr,
            )
            sys.exit(1)
        output = yaml.safe_dump(result, sort_keys=False)
    else:
        output = json_module.dumps(result, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(f"Exported: {output_path}")
    else:
        print(output)


if __name__ == "__main__":
    main()

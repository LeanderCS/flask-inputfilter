from __future__ import annotations

import sys
from pathlib import Path

import click

from ..cli import main
from ..codegen import JsonSchemaCodegen


@main.command("generate:inputfilter")
@click.option(
    "--schema",
    "schema_path",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to JSON Schema file",
)
@click.option(
    "--class",
    "class_name",
    required=True,
    help="Name of the generated InputFilter class",
)
@click.option(
    "--out",
    "out_path",
    type=click.Path(dir_okay=False),
    default="-",
    help="Output file path (- for stdout)",
)
@click.option(
    "--base-class",
    "base_class",
    default="InputFilter",
    help="Base class name for the generated class",
)
@click.option(
    "--base-module",
    "base_module",
    default="flask_inputfilter",
    help="Module to import base class from",
)
@click.option(
    "--field-import",
    "import_field_from",
    help="Module to import 'field' function from (e.g., flask_inputfilter.declarative)",
)
@click.option(
    "--field-name",
    "field_name",
    default="field",
    help="Name of the field builder function",
)
@click.option(
    "--strict", is_flag=True, help="Fail if schema properties cannot be mapped"
)
@click.option(
    "--docstring/--no-docstring",
    default=True,
    help="Include schema title and description as docstring",
)
@click.option(
    "--template",
    "template_path",
    type=click.Path(exists=True, dir_okay=False),
    default=str(
        Path(__file__).parent.parent / "templates" / "inputfilter.py.j2"
    ),
    help="Path to Jinja2 template file",
)
def generate(
    schema_path,
    class_name,
    out_path,
    base_class,
    base_module,
    import_field_from,
    field_name,
    strict,
    docstring,
    template_path,
) -> None:
    """Generate an InputFilter class from a JSON Schema file."""
    try:
        src = JsonSchemaCodegen.generate_from_file(
            schema_path=schema_path,
            class_name=class_name,
            template_path=template_path,
            base_class=base_class,
            base_module=base_module,
            import_field_from=import_field_from,
            field_name=field_name,
            strict=strict,
            docstring=docstring,
        )

        if out_path == "-":
            sys.stdout.write(src)
        else:
            Path(out_path).write_text(src, encoding="utf-8")
            click.echo(
                f"Generated InputFilter class saved to: {out_path}", err=True
            )

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

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
    "--strict", is_flag=True, help="Fail if schema properties cannot be mapped"
)
def generate_inputfilter_command(
    schema_path,
    class_name,
    out_path,
    strict,
) -> None:
    """Generate an InputFilter class from a JSON Schema file."""
    try:
        src = JsonSchemaCodegen.generate_from_file(
            schema_path=schema_path,
            class_name=class_name,
            template_path=str(Path(__file__).parent.parent / "templates" / "inputfilter.py.j2"),
            base_class="InputFilter",
            base_module="flask_inputfilter",
            strict=strict,
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

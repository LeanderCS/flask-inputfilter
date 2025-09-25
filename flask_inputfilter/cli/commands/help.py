from __future__ import annotations

import click

from ..cli import main


@main.command("help")
@click.argument("command", required=False)
def help_command(command) -> None:
    """Show help for flask-inputfilter CLI commands."""
    if command:
        ctx = click.get_current_context()
        parent_ctx = ctx.parent
        if parent_ctx and command in parent_ctx.command.commands:
            cmd = parent_ctx.command.commands[command]
            click.echo(cmd.get_help(ctx))
        else:
            click.echo(f"Unknown command: {command}")
            _show_available_commands()
    else:
        _show_general_help()


def _show_general_help() -> None:
    """Display general help with all available commands."""
    click.echo("Flask InputFilter CLI (fif) - Code Generation Tools")
    click.echo("=" * 50)
    click.echo()

    click.echo("USAGE:")
    click.echo("  fif <command> [options]")
    click.echo("  fif help [command]")
    click.echo()

    click.echo("CODE GENERATION:")
    click.echo(
        "  generate:inputfilter    Generate InputFilter classes from JSON Schema files"
    )
    click.echo()

    click.echo("UTILITIES:")
    click.echo(
        "  help                    Show this help message or help for a specific command"
    )
    click.echo()

    click.echo("EXAMPLES:")
    click.echo(
        "  fif generate:inputfilter --schema user.json --class UserInputFilter"
    )
    click.echo("  fif help generate:inputfilter")
    click.echo()

    click.echo("For detailed help on a specific command:")
    click.echo("  fif help <command>")
    click.echo()

    click.echo("Documentation: https://leandercs.github.io/flask-inputfilter")


def _show_available_commands() -> None:
    """Show just the available commands list."""
    click.echo()
    click.echo("Available commands:")
    click.echo(
        "  generate:inputfilter    Generate InputFilter classes from JSON Schema"
    )
    click.echo("  help                    Show help information")
    click.echo()
    click.echo(
        "Use 'fif help <command>' for detailed help on a specific command."
    )

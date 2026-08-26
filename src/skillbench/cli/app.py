from __future__ import annotations

from pathlib import Path

import typer

from skillbench import __version__
from skillbench.project.inspector import inspect_skill
from skillbench.project.parser import SkillParseError

app = typer.Typer(help="Local-first workbench for Agent Skills.", no_args_is_help=True)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show SkillBench version and exit.",
    ),
) -> None:
    """SkillBench command line interface."""


@app.command("inspect")
def inspect_command(path: Path = typer.Argument(Path("."), exists=True, file_okay=False)) -> None:
    """Inspect a local Agent Skill directory."""
    try:
        result = inspect_skill(path.resolve())
    except SkillParseError as exc:
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=2) from exc

    typer.echo(f"Skill: {result.name}")
    typer.echo(f"Description: {result.description}")
    typer.echo(f"SKILL.md lines: {result.line_count}")
    typer.echo(f"Approx. SKILL.md tokens: {result.skill_tokens}")
    typer.echo(f"References: {result.reference_count}")
    typer.echo(f"Scripts: {result.script_count}")
    typer.echo(f"Assets: {result.asset_count}")
    typer.echo(f"Missing references: {len(result.missing_references)}")
    typer.echo(f"Orphan references: {len(result.orphan_references)}")

    for item in result.missing_references:
        typer.echo(f"  MISSING {item}")
    for item in result.orphan_references:
        typer.echo(f"  ORPHAN {item}")

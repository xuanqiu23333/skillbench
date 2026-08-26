from pathlib import Path

from typer.testing import CliRunner

from skillbench.cli.app import app

runner = CliRunner()


def test_inspect_command_prints_skill_summary(tmp_path: Path) -> None:
    (tmp_path / "SKILL.md").write_text(
        "---\nname: demo-skill\ndescription: Demonstrate inspection.\n---\n\n# Demo\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["inspect", str(tmp_path)])

    assert result.exit_code == 0
    assert "demo-skill" in result.stdout
    assert "Demonstrate inspection." in result.stdout
    assert "Missing references: 0" in result.stdout


def test_inspect_command_returns_nonzero_for_invalid_skill(tmp_path: Path) -> None:
    result = runner.invoke(app, ["inspect", str(tmp_path)])

    assert result.exit_code != 0
    assert "SKILL.md" in result.stdout

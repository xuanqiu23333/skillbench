from pathlib import Path

from skillbench.project.inspector import inspect_skill


def test_inspect_skill_summarizes_metadata_and_resources(tmp_path: Path) -> None:
    (tmp_path / "references").mkdir()
    (tmp_path / "references" / "guide.md").write_text("12345678", encoding="utf-8")
    (tmp_path / "SKILL.md").write_text(
        "---\nname: demo-skill\ndescription: Demonstrate inspection.\n---\n\n# Demo\n\nRead references/guide.md.\n",
        encoding="utf-8",
    )

    inspection = inspect_skill(tmp_path)

    assert inspection.name == "demo-skill"
    assert inspection.description == "Demonstrate inspection."
    assert inspection.line_count >= 6
    assert inspection.skill_tokens > 0
    assert inspection.reference_count == 1
    assert inspection.missing_references == []
    assert inspection.orphan_references == []

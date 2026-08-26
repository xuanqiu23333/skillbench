from pathlib import Path

import pytest

from skillbench.project.parser import SkillParseError, parse_skill_document


def test_parse_valid_skill_document(tmp_path: Path) -> None:
    (tmp_path / "SKILL.md").write_text(
        "---\nname: systematic-debugging\ndescription: Debug failures methodically.\n---\n\n# Workflow\n\nFind the root cause.\n",
        encoding="utf-8",
    )

    document = parse_skill_document(tmp_path)

    assert document.name == "systematic-debugging"
    assert document.description == "Debug failures methodically."
    assert document.frontmatter["name"] == "systematic-debugging"
    assert "# Workflow" in document.body


def test_missing_skill_file_raises_parse_error(tmp_path: Path) -> None:
    with pytest.raises(SkillParseError, match="SKILL.md"):
        parse_skill_document(tmp_path)


def test_non_mapping_frontmatter_raises_parse_error(tmp_path: Path) -> None:
    (tmp_path / "SKILL.md").write_text("---\n- invalid\n- yaml\n---\nBody\n", encoding="utf-8")

    with pytest.raises(SkillParseError, match="mapping"):
        parse_skill_document(tmp_path)

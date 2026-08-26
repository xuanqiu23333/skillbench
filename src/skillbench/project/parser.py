from __future__ import annotations

from pathlib import Path

import yaml

from skillbench.project.models import SkillDocument


class SkillParseError(ValueError):
    """Raised when a Skill project cannot be parsed."""


def parse_skill_document(root: Path) -> SkillDocument:
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        raise SkillParseError(f"SKILL.md not found in {root}")

    raw_text = skill_path.read_text(encoding="utf-8")
    if not raw_text.startswith("---\n"):
        raise SkillParseError("SKILL.md must start with YAML frontmatter")

    try:
        _, frontmatter_text, body = raw_text.split("---", 2)
    except ValueError as exc:
        raise SkillParseError("SKILL.md frontmatter is not closed") from exc

    try:
        frontmatter = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        raise SkillParseError(f"Invalid YAML frontmatter: {exc}") from exc

    if not isinstance(frontmatter, dict):
        raise SkillParseError("SKILL.md frontmatter must be a mapping")

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not isinstance(name, str) or not name.strip():
        raise SkillParseError("SKILL.md frontmatter requires a non-empty name")
    if not isinstance(description, str) or not description.strip():
        raise SkillParseError("SKILL.md frontmatter requires a non-empty description")

    return SkillDocument(
        path=skill_path,
        frontmatter=frontmatter,
        body=body.lstrip("\n"),
        name=name.strip(),
        description=description.strip(),
        raw_text=raw_text,
    )

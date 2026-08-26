from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


class SkillDocument(BaseModel):
    path: Path
    frontmatter: dict[str, Any]
    body: str
    name: str
    description: str
    raw_text: str


class SkillResource(BaseModel):
    path: str
    kind: Literal["reference", "script", "asset"]
    exists: bool
    referenced_from_skill: bool
    approx_tokens: int | None = None


class SkillInspection(BaseModel):
    root_path: Path
    name: str
    description: str
    line_count: int
    skill_tokens: int
    resources: list[SkillResource] = Field(default_factory=list)
    reference_count: int = 0
    script_count: int = 0
    asset_count: int = 0
    missing_references: list[str] = Field(default_factory=list)
    orphan_references: list[str] = Field(default_factory=list)

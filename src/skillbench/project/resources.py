from __future__ import annotations

import math
import re
from pathlib import Path

from skillbench.project.models import SkillResource

RESOURCE_PATTERN = re.compile(
    r"(?P<path>(?:references|scripts|assets)/[A-Za-z0-9_./-]+)"
)
RESOURCE_DIRS = {
    "references": "reference",
    "scripts": "script",
    "assets": "asset",
}
TEXT_SUFFIXES = {".md", ".txt", ".py", ".json", ".yaml", ".yml", ".toml", ".js", ".ts"}


def _normalize_resource_path(value: str) -> str:
    return value.rstrip(".,;:!?)]}`\"'")


def _approx_tokens(path: Path) -> int | None:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    return math.ceil(len(text) / 4)


def inspect_resources(root: Path, body: str) -> list[SkillResource]:
    referenced_paths = {
        _normalize_resource_path(match.group("path"))
        for match in RESOURCE_PATTERN.finditer(body)
    }

    existing_paths: set[str] = set()
    for dirname in RESOURCE_DIRS:
        directory = root / dirname
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if path.is_file():
                existing_paths.add(path.relative_to(root).as_posix())

    all_paths = sorted(existing_paths | referenced_paths)
    resources: list[SkillResource] = []
    for relative_path in all_paths:
        top_level = relative_path.split("/", 1)[0]
        kind = RESOURCE_DIRS[top_level]
        full_path = root / relative_path
        exists = full_path.is_file()
        resources.append(
            SkillResource(
                path=relative_path,
                kind=kind,
                exists=exists,
                referenced_from_skill=relative_path in referenced_paths,
                approx_tokens=_approx_tokens(full_path) if exists else None,
            )
        )

    return resources

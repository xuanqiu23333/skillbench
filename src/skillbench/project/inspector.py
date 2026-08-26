from __future__ import annotations

import math
from pathlib import Path

from skillbench.project.models import SkillInspection
from skillbench.project.parser import parse_skill_document
from skillbench.project.resources import inspect_resources


def inspect_skill(root: Path) -> SkillInspection:
    document = parse_skill_document(root)
    resources = inspect_resources(root, document.body)

    return SkillInspection(
        root_path=root,
        name=document.name,
        description=document.description,
        line_count=len(document.raw_text.splitlines()),
        skill_tokens=math.ceil(len(document.raw_text) / 4),
        resources=resources,
        reference_count=sum(resource.kind == "reference" for resource in resources if resource.exists),
        script_count=sum(resource.kind == "script" for resource in resources if resource.exists),
        asset_count=sum(resource.kind == "asset" for resource in resources if resource.exists),
        missing_references=[
            resource.path for resource in resources if resource.referenced_from_skill and not resource.exists
        ],
        orphan_references=[
            resource.path
            for resource in resources
            if resource.kind == "reference" and resource.exists and not resource.referenced_from_skill
        ],
    )

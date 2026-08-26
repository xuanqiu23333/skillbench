from pathlib import Path

from skillbench.project.resources import inspect_resources


def test_detects_referenced_missing_and_orphan_resources(tmp_path: Path) -> None:
    (tmp_path / "references").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "references" / "used.md").write_text("Used reference", encoding="utf-8")
    (tmp_path / "references" / "orphan.md").write_text("Orphan reference", encoding="utf-8")
    (tmp_path / "scripts" / "check.py").write_text("print('ok')\n", encoding="utf-8")

    body = (
        "Read [the guide](references/used.md), then run `scripts/check.py`. "
        "Also consult references/missing.md."
    )

    resources = inspect_resources(tmp_path, body)
    by_path = {resource.path: resource for resource in resources}

    assert by_path["references/used.md"].exists is True
    assert by_path["references/used.md"].referenced_from_skill is True
    assert by_path["references/orphan.md"].exists is True
    assert by_path["references/orphan.md"].referenced_from_skill is False
    assert by_path["scripts/check.py"].kind == "script"
    assert by_path["references/missing.md"].exists is False
    assert by_path["references/missing.md"].referenced_from_skill is True


def test_text_resource_gets_approximate_token_count(tmp_path: Path) -> None:
    (tmp_path / "references").mkdir()
    (tmp_path / "references" / "short.md").write_text("abcdefgh", encoding="utf-8")

    resources = inspect_resources(tmp_path, "references/short.md")
    resource = next(item for item in resources if item.path == "references/short.md")

    assert resource.approx_tokens == 2

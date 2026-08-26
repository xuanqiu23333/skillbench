# SkillBench

> A local-first workbench for testing and debugging Agent Skills.

**Status:** Pre-alpha · CLI alpha under active development

SkillBench is an open-source developer tool for building, inspecting, testing, and comparing Agent Skills locally. It is designed to make the Skill development loop visible and reproducible instead of forcing developers to jump between Markdown files, terminal logs, eval JSON, and ad-hoc scripts.

## Why SkillBench?

Agent Skills package instructions, scripts, references, and assets for coding agents and other AI agents. The surrounding development workflow is still fragmented: authors need to inspect structure, understand context cost, manage eval cases, run skills against agents, compare with/without-skill behavior, and catch regressions.

SkillBench aims to provide one local-first workbench for that loop.

## Current CLI alpha scope

The first implementation slice focuses on local inspection:

- Parse `SKILL.md` YAML frontmatter and Markdown body
- Inspect `references/`, `scripts/`, and `assets/`
- Detect referenced, missing, and orphan reference files
- Estimate local text context size with a lightweight heuristic
- Expose the result through `skillbench inspect PATH`
- Verify behavior with pytest, ruff, and GitHub Actions

Eval execution, Codex integration, comparison, persistence, and the web UI remain planned v0.1 work and are **not implemented yet**.

## Local development environment

The primary development setup mirrors the existing Hongkong project workflow:

- Windows 11 host
- dedicated Conda environment: `skillbench`
- Python 3.11
- Codex runs on the host machine
- Docker is not required for SkillBench v0.1

Create and prepare the environment:

```powershell
conda create -n skillbench python=3.11 -y
conda run -n skillbench python -m pip install -e ".[dev]"
```

Inspect the included valid example Skill:

```powershell
conda run -n skillbench skillbench inspect examples/good-skill
```

Run quality checks:

```powershell
conda run -n skillbench ruff check .
conda run -n skillbench pytest -q
```

## Planned v0.1

- Inspect `SKILL.md` metadata and project structure
- Analyze references and approximate context/token budget
- Read and manage `evals/evals.json`
- Run eval cases through an adapter interface
- Start with a Codex adapter, with room for more agents later
- Compare with-skill vs. without-skill runs
- Store local run history and metrics
- Provide a headless CLI mode for CI
- Provide a local web UI for Overview, Context, Evals, Runs, and Compare

## Product principles

- **Local-first:** Skill source files and run artifacts stay on the developer machine by default.
- **Open-standard friendly:** Prefer compatibility with existing Agent Skills conventions and eval formats over inventing new ones.
- **Small core, extensible adapters:** Avoid bundling every agent integration into the core.
- **Observable by default:** A developer should be able to understand why a Skill helped, hurt, or failed to trigger.
- **No fake complexity:** SQLite/filesystem before distributed infrastructure; no cloud account required for v0.1.

## Concept

```text
Skill directory
    │
    ├── SKILL.md
    ├── scripts/
    ├── references/
    ├── assets/
    └── evals/evals.json
            │
            ▼
        SkillBench
      ┌─────┼──────────────┐
      │     │              │
  Inspector Eval Runner  Run History
      │     │              │
      └─────┼──────────────┘
            ▼
        Compare View
  without skill ↔ with skill
```

## Target CLI contract

```bash
skillbench inspect .
skillbench run . --agent codex
skillbench test . --headless
skillbench open .
```

Only `inspect` belongs to the current CLI alpha implementation slice.

## Documentation

- [`docs/PRD.md`](docs/PRD.md) — product requirements for v0.1
- [`docs/architecture.md`](docs/architecture.md) — proposed technical architecture
- [`docs/roadmap.md`](docs/roadmap.md) — staged delivery roadmap
- [`docs/superpowers/plans/2026-08-26-v0.1-cli-alpha.md`](docs/superpowers/plans/2026-08-26-v0.1-cli-alpha.md) — first implementation plan

## Contributing

The repository is in early development. Small, testable changes that preserve the local-first and open-standard-friendly direction are preferred.

## License

MIT License.

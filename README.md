# SkillBench

> A local-first workbench for testing and debugging Agent Skills.

**Status:** Pre-alpha · design and bootstrap phase

SkillBench is an open-source developer tool for building, inspecting, testing, and comparing Agent Skills locally. It is designed to make the Skill development loop visible and reproducible instead of forcing developers to jump between Markdown files, terminal logs, eval JSON, and ad-hoc scripts.

## Why SkillBench?

Agent Skills are becoming a reusable way to package instructions, scripts, references, and assets for coding agents and other AI agents. The surrounding development workflow is still fragmented: authors need to inspect structure, understand context cost, manage eval cases, run skills against agents, compare with/without-skill behavior, and catch regressions.

SkillBench aims to provide one local-first workbench for that loop.

## Planned v0.1

- Inspect `SKILL.md` metadata and project structure
- Analyze references and approximate context/token budget
- Read and manage `evals/evals.json`
- Run eval cases through an adapter interface
- Start with a Codex adapter, with room for more agents later
- Compare with-skill vs. without-skill runs
- Store local run history and metrics
- Provide a headless CLI mode for CI

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

## Intended CLI

The v0.1 interface is being designed around commands such as:

```bash
skillbench inspect .
skillbench run . --agent codex
skillbench test . --headless
skillbench open .
```

These commands are part of the product contract under design and are not yet released.

## Documentation

- [`docs/PRD.md`](docs/PRD.md) — product requirements for v0.1
- [`docs/architecture.md`](docs/architecture.md) — proposed technical architecture
- [`docs/roadmap.md`](docs/roadmap.md) — staged delivery roadmap

## Contributing

The repository is in its design/bootstrap phase. Issues and implementation tasks will be opened after the v0.1 product contract is locked.

## License

MIT License.

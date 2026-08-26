# SkillBench Roadmap

## Guiding rule

Ship the smallest complete developer loop first. Each release should remain usable on its own and avoid speculative infrastructure.

## v0.1 — Local Skill inspection and comparison

Goal: prove the core product loop.

Planned scope:

- Skill project discovery and `SKILL.md` parsing
- frontmatter and local resource inspection
- approximate token/context analysis
- `evals/evals.json` loading
- adapter abstraction
- Codex adapter
- baseline vs. with-skill execution
- local run persistence
- CLI comparison output
- headless CI mode
- local web UI with Overview, Context, Evals, Runs, Compare

Release gate:

- end-to-end run works locally on at least one example Skill;
- comparison artifacts are reproducible;
- core test suite passes in CI;
- no cloud account or external SkillBench service is required.

## v0.2 — Better eval authoring and regression workflows

Potential scope after v0.1 feedback:

- richer eval editor
- deterministic assertion presets
- run tags and notes
- compare any two historical runs
- configurable quality thresholds
- Git diff awareness for Skill changes
- improved CI report output

## v0.3 — Ecosystem integrations

Only after real usage demonstrates need:

- second agent adapter
- external validator integration
- import/export bridges for popular Skill tooling
- reusable adapter contribution guide

## Later / intentionally deferred

These are explicitly not near-term commitments:

- hosted SaaS
- user accounts
- team workspaces
- marketplace/registry
- payments
- remote execution workers
- general LLM observability platform
- automatic Skill generation
- broad plugin framework

## Open-source milestones

### Milestone A — Design locked

- README
- PRD
- architecture
- roadmap
- initial implementation plan

### Milestone B — CLI alpha

- `skillbench inspect`
- eval loading
- fake adapter test harness
- local persistence
- Codex adapter
- baseline/treatment run comparison

### Milestone C — Local UI alpha

- FastAPI local server
- Overview
- Context
- Evals
- Runs
- Compare

### Milestone D — v0.1.0

- CI/headless workflow
- examples
- installation docs
- contribution guide
- release notes

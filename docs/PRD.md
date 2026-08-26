# SkillBench v0.1 Product Requirements Document

## 1. Product summary

SkillBench is a local-first workbench for developing, testing, debugging, and comparing Agent Skills.

The v0.1 goal is not to become another Skill marketplace, validator-only CLI, or general LLM observability platform. It focuses on one developer loop:

> inspect a Skill → understand its context footprint → run evals → compare with/without-skill behavior → detect regressions.

## 2. Target users

Primary users:

- Independent AI developers authoring Agent Skills
- Developers using Codex or similar coding agents locally
- Open-source maintainers who want repeatable Skill evaluation
- Teams experimenting with reusable agent instructions before adopting heavier infrastructure

## 3. Core problem

Today, Skill development is fragmented across:

- `SKILL.md`
- `scripts/`, `references/`, and `assets/`
- eval JSON files
- terminal commands and agent logs
- manual comparison of outputs
- ad-hoc notes about token usage, regressions, and trigger behavior

This makes it hard to answer basic questions:

1. Is this Skill structurally valid?
2. What context does it load and how large is it?
3. Which files are referenced, missing, or unused?
4. Does the Skill materially improve an agent's performance?
5. Did a recent Skill change introduce a regression?

## 4. Product positioning

SkillBench is:

- a local developer workbench
- compatible with existing Skill conventions where practical
- focused on comparison and debugging
- usable from both CLI and local web UI

SkillBench is not, in v0.1:

- a hosted SaaS
- a Skill marketplace
- a Skill generator
- a universal agent platform
- a replacement for full observability systems
- a replacement for every existing validator or benchmark tool

## 5. v0.1 success criteria

A developer can point SkillBench at a local Skill directory and complete the following loop without writing custom glue code:

1. inspect the Skill structure;
2. see metadata, reference health, and approximate context size;
3. load eval cases from `evals/evals.json`;
4. run a selected eval through the Codex adapter;
5. run the same eval with the Skill disabled;
6. compare outputs and execution metrics;
7. persist run artifacts locally;
8. run the same checks headlessly in CI.

## 6. Functional requirements

### FR-1 Skill discovery and parsing

Given a path to a Skill directory, SkillBench must:

- locate `SKILL.md`;
- parse YAML frontmatter;
- parse Markdown body;
- enumerate `scripts/`, `references/`, `assets/`, and `evals/` when present;
- surface parse errors without crashing the whole application.

### FR-2 Static inspection

SkillBench must report:

- Skill name and description;
- frontmatter validity;
- SKILL.md line count;
- approximate token count;
- referenced local files;
- missing references;
- existing but unreferenced files under `references/`;
- script/reference/asset counts.

Built-in checks should remain intentionally small. External validators may be integrated later through adapters rather than reimplemented wholesale.

### FR-3 Context inspector

SkillBench must represent the Skill as three context levels:

1. metadata (`name`, `description`);
2. `SKILL.md` body;
3. references/scripts/assets loaded on demand.

The UI and CLI should show approximate token contribution for each textual context source.

### FR-4 Eval format

v0.1 must read `evals/evals.json`.

Each eval case must support at minimum:

- `id`
- `prompt`
- optional `expected_output`
- optional `files`

SkillBench should preserve unknown fields when editing where feasible so that it does not unnecessarily break compatibility with upstream tooling.

### FR-5 Agent adapter contract

v0.1 must define a stable adapter interface and ship one production adapter:

- Codex adapter

The adapter interface must separate:

- availability check;
- run invocation;
- normalized result collection;
- metrics collection.

Additional agents are out of scope for v0.1.

### FR-6 With-skill / without-skill comparison

For a selected eval case, SkillBench must be able to create two runs:

- baseline: Skill disabled;
- treatment: Skill enabled.

The comparison must show, where available:

- completion status;
- duration;
- output;
- tool-call count;
- token information;
- assertion results;
- errors.

### FR-7 Run history

Each run must receive a unique local run ID and persist:

- run metadata;
- prompt;
- normalized output;
- stdout/stderr when available;
- metrics;
- grading/assertion results.

Large textual artifacts should live on the filesystem. SQLite stores searchable run metadata.

### FR-8 CLI

v0.1 command contract:

```bash
skillbench inspect PATH
skillbench run PATH --agent codex
skillbench test PATH --headless
skillbench open PATH
```

Exit codes for `test --headless` must be CI-friendly:

- `0`: checks passed;
- non-zero: invalid Skill, failed required assertions, adapter failure, or configured quality threshold not met.

### FR-9 Local web UI

The local web UI must provide five views:

- Overview
- Context
- Evals
- Runs
- Compare

The UI is a local development interface, not a hosted account-based application.

## 7. Non-functional requirements

### NFR-1 Local-first privacy

Skill source files and run artifacts stay local by default. SkillBench must not require a SkillBench cloud account.

### NFR-2 Minimal infrastructure

v0.1 uses:

- filesystem
- SQLite

It must not require Redis, Kafka, PostgreSQL, vector databases, Kubernetes, or other distributed infrastructure.

### NFR-3 Extensibility

Agent integrations must use adapters so new agents can be contributed without changing the core eval model.

### NFR-4 Failure transparency

Errors must distinguish at minimum:

- Skill parse error;
- eval parse error;
- adapter unavailable;
- agent execution failure;
- timeout;
- assertion failure;
- local persistence failure.

### NFR-5 Testability

Core parsing, analysis, comparison, and persistence behavior must be testable without launching a real external agent process.

## 8. Data model

### SkillProject

- `root_path: Path`
- `name: str`
- `description: str`
- `skill_markdown: str`
- `frontmatter: dict`
- `resources: list[SkillResource]`
- `eval_suite: EvalSuite | None`

### SkillResource

- `path: str`
- `kind: reference | script | asset`
- `exists: bool`
- `referenced_from_skill: bool`
- `approx_tokens: int | None`

### EvalCase

- `id: str | int`
- `prompt: str`
- `expected_output: str | None`
- `files: list[str]`
- `extra: dict`

### AgentRun

- `run_id: str`
- `skill_name: str`
- `eval_id: str`
- `mode: baseline | with_skill`
- `agent: str`
- `started_at: datetime`
- `duration_ms: int | None`
- `status: passed | failed | error`
- `output_path: str | None`
- `stdout_path: str | None`
- `stderr_path: str | None`
- `metrics: dict`
- `error: str | None`

### Comparison

- `baseline_run_id: str`
- `skill_run_id: str`
- `metric_deltas: dict`
- `assertion_deltas: dict`

## 9. Storage layout

SkillBench local state lives under the target Skill directory by default:

```text
.skillbench/
├── skillbench.db
└── runs/
    └── <run-id>/
        ├── run.json
        ├── prompt.txt
        ├── output.md
        ├── stdout.log
        ├── stderr.log
        ├── metrics.json
        └── grading.json
```

`.skillbench/` should be added to `.gitignore` by users unless they intentionally want to version run artifacts.

## 10. Out of scope for v0.1

- hosted accounts
- cloud synchronization
- billing
- team workspaces
- marketplace or registry
- automatic Skill generation
- remote execution service
- more than one built-in production agent adapter
- distributed workers
- arbitrary LLM gateway
- proprietary Skill file format

## 11. Release definition

v0.1.0 is ready when:

- `skillbench inspect` works on good and malformed example Skills;
- Codex adapter availability is detected cleanly;
- one eval can be executed in baseline and with-skill modes;
- both runs persist locally;
- compare output is available through CLI/API;
- the five local UI views can consume the same backend models;
- `skillbench test --headless` returns reliable CI exit codes;
- core test suite and CI pass on the supported Python version.

# SkillBench v0.1 Technical Architecture

## 1. Architecture goals

SkillBench should stay small, local-first, observable, and easy to extend. The architecture separates parsing/analysis, eval execution, adapters, persistence, API, and UI so each part can be tested independently.

## 2. Proposed stack

Backend and CLI:

- Python 3.12
- FastAPI
- Pydantic 2
- Typer
- SQLAlchemy 2
- SQLite
- pytest
- ruff

Frontend:

- React
- TypeScript
- Vite

Transport:

- REST for CRUD/query operations
- SSE for long-running run progress where needed

## 3. High-level architecture

```text
                         Browser
                            │
                            ▼
                    React + TypeScript
                            │
                     REST / optional SSE
                            │
                            ▼
                         FastAPI
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 Skill Project Core      Eval Engine        Run Store
        │                   │                   │
        ▼                   ▼                   ▼
 Parser / Analyzer      Agent Adapter       SQLite + FS
        │                   │
        │                ┌──┴──┐
        │                ▼     ▼
        │              Codex  Future
        │
        ▼
 SKILL.md / refs /
 scripts / assets
```

## 4. Core boundaries

### 4.1 Skill project core

Responsibilities:

- discover a Skill project;
- parse `SKILL.md` frontmatter/body;
- enumerate resources;
- identify missing and unreferenced resources;
- estimate textual context size;
- expose normalized Pydantic models.

The core must not depend on FastAPI or React.

### 4.2 Eval engine

Responsibilities:

- load `evals/evals.json`;
- normalize eval cases;
- orchestrate baseline and with-skill runs;
- run assertions/grading hooks;
- produce normalized run/comparison models.

The eval engine must depend on the abstract adapter contract, not Codex-specific implementation details.

### 4.3 Agent adapter layer

A minimal adapter contract should look conceptually like:

```python
class AgentAdapter(Protocol):
    name: str

    async def check_available(self) -> AdapterAvailability:
        ...

    async def run(self, request: AgentRunRequest) -> AgentRunResult:
        ...
```

The Codex adapter is the only production adapter required for v0.1.

Adapter responsibilities:

- detect whether its local CLI/runtime is available;
- translate normalized requests to agent-specific invocation;
- enforce timeout/cancellation boundaries;
- capture stdout/stderr;
- normalize result/metrics.

Adapters must not write directly to SQLite.

### 4.4 Run storage

Use two storage forms:

1. SQLite for searchable metadata and indexes;
2. filesystem for outputs/logs/metrics JSON.

This avoids storing large text blobs in the database while keeping local inspection simple.

### 4.5 HTTP API

FastAPI is a thin orchestration layer over core services. API routes must not contain parsing, grading, or adapter logic.

Suggested API groups:

```text
/api/project
/api/evals
/api/runs
/api/comparisons
/api/system
```

### 4.6 Web UI

Five v0.1 views:

- Overview — project health and summary;
- Context — context levels, resources, token estimates;
- Evals — eval cases and edit flow;
- Runs — run history and status;
- Compare — baseline vs. with-skill comparison.

The UI consumes normalized backend models and must not parse `SKILL.md` itself.

## 5. Proposed repository layout

```text
skillbench/
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
├── docs/
│   ├── PRD.md
│   ├── architecture.md
│   └── roadmap.md
├── src/
│   └── skillbench/
│       ├── cli/
│       ├── project/
│       ├── evals/
│       ├── adapters/
│       ├── runs/
│       └── server/
├── web/
│   └── src/
├── tests/
├── examples/
│   ├── good-skill/
│   └── bad-skill/
└── .github/
    └── workflows/
```

## 6. Proposed internal modules

### `project/`

- `models.py` — normalized Skill project models
- `parser.py` — SKILL.md parsing
- `resources.py` — resource discovery/reference checks
- `tokens.py` — approximate textual token estimation

### `evals/`

- `models.py` — eval suite/case models
- `loader.py` — load/preserve eval JSON
- `runner.py` — baseline/treatment orchestration
- `assertions.py` — deterministic assertion layer
- `compare.py` — normalized comparison/deltas

### `adapters/`

- `base.py` — adapter protocol/base models
- `codex.py` — Codex CLI/runtime integration

### `runs/`

- `models.py` — run metadata
- `repository.py` — SQLite metadata persistence
- `artifacts.py` — filesystem artifact persistence

### `server/`

- `app.py` — FastAPI app factory
- route modules grouped by product capability

## 7. Data flow: inspect

```text
CLI/UI request
   ↓
SkillProjectService
   ↓
SKILL.md parser
   + resource scanner
   + token estimator
   ↓
SkillProject model
   ↓
CLI formatter / FastAPI response
```

## 8. Data flow: run and compare

```text
EvalCase
   ↓
EvalRunner
   ├── baseline request ─────┐
   └── with-skill request ──┤
                            ▼
                       AgentAdapter
                            │
                            ▼
                     normalized results
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
        RunArtifactStore              RunRepository
          filesystem                     SQLite
              └─────────────┬─────────────┘
                            ▼
                         Compare
```

## 9. Error model

Normalize failures into explicit categories:

```text
SkillParseError
EvalFormatError
AdapterUnavailableError
AgentExecutionError
AgentTimeoutError
AssertionFailure
PersistenceError
```

A failed run should still persist diagnostic artifacts when possible.

## 10. Security and local execution boundaries

SkillBench may launch external agent processes. v0.1 therefore must:

- clearly show which adapter/command is being used;
- impose configurable execution timeout;
- avoid silently escalating privileges;
- avoid collecting source files outside the selected Skill/project scope unless the user explicitly passes them to an eval;
- redact or avoid logging environment secrets where possible;
- treat agent stdout/stderr as untrusted text.

## 11. Testing strategy

Core project/eval behavior follows test-first development.

Test layers:

1. unit tests for parser/resource analysis/eval loader/comparison;
2. persistence tests using temporary filesystem and SQLite;
3. adapter contract tests using a deterministic fake adapter;
4. Codex adapter availability/invocation tests that mock only the process boundary;
5. FastAPI route tests against the same core services;
6. frontend tests after the backend contracts stabilize.

Real Codex execution should be an opt-in integration test, not required for normal CI.

## 12. CI strategy

Initial CI should validate:

- supported Python setup;
- dependency installation;
- ruff checks;
- pytest suite.

Frontend CI can be added when the web package exists; do not add failing placeholder jobs before then.

## 13. Extension model after v0.1

Future additions should enter through explicit extension boundaries:

- new agents → adapter layer;
- external validators → analyzer integration;
- new graders → assertion/grading interface;
- new run exporters → run storage/export interface.

Avoid introducing a general plugin system until at least two real external integrations demonstrate a stable need.

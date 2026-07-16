# QA Case Pipeline

`qa-case-pipeline` is an open research prototype for turning a **sanitized QA
brief** into a reviewable four-stage testing package:

1. analysis of scope and regression risk;
2. a verification algorithm and required evidence;
3. repeatable automated checks;
4. manual exploratory checks beyond automation.

The project is based on a practical QA approach used for complex delivery
work: make the test logic explicit before execution, preserve evidence, and
keep manual investigation as a separate professional activity. It does not
claim that an LLM, a fixture, or a successful script can replace production
validation or a QA engineer's judgment.

## Why This Exists

Complex changes often span requirements, data contracts, UI state, and legacy
behavior. When these concerns live in scattered notes, ad-hoc scripts, and
individual browser sessions, coverage is difficult to review and reproduce.

This prototype creates one traceable package: the reasoning, the algorithm,
the deterministic evidence, and the remaining human exploration. The initial
examples are fully synthetic and focus on two common high-risk patterns:

- preserving UI state and URL parameters across navigation;
- keeping legacy records safe during a composite-key migration.

Read the detailed approach in [docs/methodology.md](docs/methodology.md).

## Quick Start

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --group dev
uv run qa-case-pipeline demo --case ui-state-persistence --output ./artifacts/ui-state
uv run qa-case-pipeline validate \
  --case src/qa_case_pipeline/fixtures/schema-legacy-compat
uv run pytest
```

The demo writes `analysis.md`, `algorithm.md`, `automated-checks.md`,
`manual-checks.md`, a structured `qa-plan.json`, synthetic inputs, and
reference-check evidence. Add `--language ru` to create Russian-language
artifacts.

## Generate a Plan with Codex

The `plan` command uses a locally authenticated Codex CLI and enforces a JSON
schema for its result. It runs Codex in a temporary directory with read-only
sandboxing; it does not pass a repository path or execute a target project's
tests.

```bash
codex login
uv run qa-case-pipeline plan \
  --brief src/qa_case_pipeline/fixtures/ui-state-persistence/brief.yaml \
  --output ./artifacts/generated-plan \
  --language en
```

The input brief must be safe for public use. Do not include credentials,
customer data, private URLs, proprietary source code, or internal issue links.
Review every generated artifact before using it in a real project.

## Project Layout

```text
src/qa_case_pipeline/
  cli.py                 Command-line interface
  codex_adapter.py       Constrained Codex CLI integration
  models.py              Sanitized brief validation
  reference_checks.py    Deterministic fixture checks
  renderer.py            Markdown and JSON artifact rendering
  fixtures/              Fully synthetic examples
  schemas/               Structured model-output contract
tests/                   Unit and CLI tests
docs/methodology.md      Methodology and safety boundaries
```

## Local Configuration and Git Workflow

Create `.env` from `.env.example` only when the project needs local variables.
It is not tracked by Git. GitHub access uses the GitHub CLI (`gh`); no token is
stored in this repository.

The default branch is `main`. Significant agreed changes are tested, committed,
pushed to `origin/main`, and then verified remotely. Repository rules and the
GitHub-growth checklist are maintained in [AGENTS.md](AGENTS.md) and
[docs/github-growth.md](docs/github-growth.md).

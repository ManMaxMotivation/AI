# QA Case Pipeline

Turn a risky product change into a QA package that another engineer can review,
run, and audit.

`qa-case-pipeline` is for QA engineers, SDETs, developers, and delivery leads
who need more than a checklist. It connects four things that are often kept
apart: the requirement, the verification algorithm, repeatable evidence checks,
and the manual exploration that automation cannot honestly replace.

It is useful when a small-looking change crosses several layers: a service
state, a static or cached page, desktop and mobile controls, legacy data, or a
transition window between systems.

## What You Get

For one case directory, the tool produces:

| Stage | Artifact | Why it matters |
| --- | --- | --- |
| Analysis | `artifacts/analysis.md` | Scope, acceptance criteria, risks, constraints, and traceable requirements. |
| Algorithm | `artifacts/algorithm.md` | The evidence collection and verification sequence. |
| Automation | `artifacts/automated-report.md` | Reproducible pass/fail assertions over local JSON evidence. |
| Manual QA | `artifacts/manual-checks.md` and `artifacts/qa-report.md` | Exploratory scenarios and an explicit record of what a person actually checked. |

The final report maps every requirement to automated and manual evidence. It
never calls itself a release approval: a human still makes that decision.

## See a Complete Case First

Python 3.12+ and [uv](https://docs.astral.sh/uv/) are required.

```bash
git clone https://github.com/ManMaxMotivation/AI.git
cd AI
uv run qa-case-pipeline demo \
  --case reservation-state-propagation \
  --output ./demo-reservation-case
```

Open `demo-reservation-case/artifacts/qa-report.md`. The synthetic case executes
seven declared automated checks and shows four completed manual records for a
realistic failure mode: an item becomes reserved, checkout rejects it before a
cached page has refreshed, and the old page must not keep an active purchase
action.

The example is synthetic. It contains no production endpoint, customer data,
credentials, private issue, or proprietary code.

## Use It on Your Own Change

Create an editable case from the same template:

```bash
uv run qa-case-pipeline init \
  --template reservation-state-propagation \
  --output ./cases/reservation-state
```

Edit these files before treating the result as evidence:

```text
cases/reservation-state/
  brief.yaml                 Change, acceptance criteria, risks, constraints
  verification.yaml          Requirements and declarative automated assertions
  evidence/*.json            Sanitized exports from approved test tooling
  manual-results.yaml        What a tester actually observed
```

Then run the case:

```bash
uv run qa-case-pipeline prepare --case ./cases/reservation-state
uv run qa-case-pipeline verify --case ./cases/reservation-state
uv run qa-case-pipeline report --case ./cases/reservation-state
```

`report` returns a non-zero exit code while an automated check fails or any
manual check remains `not_run`, `blocked`, or `failed`. This makes it suitable
for a CI step after your existing approved test jobs export evidence files.

## How Evidence Verification Works

You keep the test execution where it belongs: in your approved unit, API,
Playwright, data, or browser tooling. Export the facts needed for acceptance as
local JSON and declare the assertions in `verification.yaml`.

```yaml
evidence:
  reserved_page: evidence/reserved-page.json
automated_checks:
  - id: AUTO-003
    requirement: R-002
    purpose: Reserved desktop action cannot open checkout.
    source: reserved_page
    assertions:
      - pointer: /ui/desktop_action/enabled
        operator: equals
        value: false
      - pointer: /ui/desktop_action/href
        operator: exists
        value: false
```

The verifier uses standard JSON Pointers and supports `equals`, `not_equals`,
`exists`, `contains`, and `matches`. It reads only JSON files inside the case
directory. It does not run arbitrary shell commands, execute a target project,
or access the network.

## The Included Realistic Template

`reservation-state-propagation` is an anonymized model of a complex delivery
case. It covers:

- available, reserved, and unavailable state contracts;
- desktop, mobile, and comparison-page actions;
- preservation of the existing available-item path;
- the dangerous interval where checkout and page data disagree;
- manual visual, keyboard, mobile, and end-to-end exploration.

Replace the wording, requirements, local evidence exports, and manual results
with your own sanitized case. The template deliberately starts manual results
as `not_run`, so a copied case cannot accidentally be reported as complete.

## Optional Codex Drafting

For a sanitized brief, Codex can draft the four-stage plan as structured JSON:

```bash
codex login
uv run qa-case-pipeline plan \
  --brief ./cases/reservation-state/brief.yaml \
  --output ./drafted-plan
```

This is a drafting aid, not the evidence engine. The command runs Codex in an
empty temporary directory with read-only sandboxing and validates its output
against a JSON Schema. Review the draft, then express the checks you truly need
in `verification.yaml`.

## Boundaries

- Do not put credentials, private URLs, customer data, internal issue links, or
  proprietary source code in a public case.
- A passing report means the declared local evidence and recorded manual checks
  are complete. It does not prove a production release is safe.
- This tool does not replace product requirements, observability, security
  review, or exploratory QA.

For the methodology behind the workflow, see
[docs/methodology.md](docs/methodology.md). Repository workflow and the
GitHub-growth register are documented in [AGENTS.md](AGENTS.md) and
[docs/github-growth.md](docs/github-growth.md).

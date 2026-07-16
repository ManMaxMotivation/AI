---
name: ai-assisted-qa
description: "Guide a QA agent through a four-stage workflow for complex product changes: scope analysis, risk-based verification algorithm, automated evidence, manual exploratory testing, and traceable reporting. Use when asked to analyze a task, pull request, code change, bug fix, release candidate, data migration, API contract, UI behavior, or to create test cases and QA reports."
---

# AI-Assisted QA

Create a factual, reviewable QA artifact chain. Do not jump directly from a
task description to test execution or a verdict.

## Human-Gated Session Mode

Use staged sessions by default. Run only the phase the user explicitly requests;
do not continue to the next phase because a prior artifact looks complete. This
lets the engineer inspect the agent's understanding and correct it before later
work depends on it.

1. **Analysis**: establish scope and risk.
2. **Algorithm**: agree the reproducible verification route.
3. **Automated evidence**: prepare and, when authorized, run the relevant
   checks.
4. **Manual test case**: prepare human scenarios from the approved prior work.

Show the complete phase artifact in chat first. Save only the same approved
content, without silent rewriting. Create a final report only after execution
evidence exists and the user requests reporting.

Use `references/staged-session-prompts.md` for copyable phase prompts.

## Required Inputs

Collect the available task description, acceptance criteria or DoD, changed
code or pull request, existing tests, relevant configurations, and prior
artifacts. Identify missing sources explicitly. Do not invent requirements,
environment state, execution results, or access.

Before reading or publishing material, apply the privacy rules in
`references/publication-safety.md`.

If the project has route memory, read it before route discovery. Use the
`references/route-memory.md` protocol: find a proven matching route, compare it
with the current task, reuse it where valid, and update or add it only after a
new route is proven.

## Workflow

### 1. Analyze the Full Scope

Create `analysis.md` using the artifact contract. Establish:

- the change in plain language and its acceptance criteria;
- the source of truth for each requirement;
- changed components, data contracts, routes, state transitions, and dependent
  systems;
- regression zones and a risk reason for each one;
- constraints, unknowns, and blockers.

Read the changed code and relevant existing tests before selecting coverage.
Do not replace the described scope with a happy path or representative subset
unless the analysis states why that subset covers the changed risk.

### 2. Build the Verification Algorithm

Create `algorithm.md` before executing checks. Define an ordered route from
preconditions to observable outcomes. For every step state:

- requirement or risk addressed;
- system layer and approved tool or entry point;
- expected evidence;
- stop condition or handoff needed.

Use `references/risk-patterns.md` when the task involves state propagation, UI
state, contracts, legacy data, asynchronous processing, or cross-system flows.

After the task route is built, synchronize route memory using
`compare -> reuse/update/add`. Keep one-off root causes in the task artifact and
repeatable process barriers in a separate barrier record; neither belongs in a
reusable route map by default.

### 3. Produce Automated Evidence

Create `automated-checks.md`. Prefer the project's existing test runner and
approved environment. Select the narrowest test layer that proves the behavior:
unit, contract, API, integration, data, or browser.

Record the exact scope, command or procedure, evidence location, and factual
outcome. A green check proves only what it observed. If a required check cannot
run, record the blocker and its impact; do not convert it into a pass.

Do not run destructive production operations, publish data, or execute
unreviewed commands merely to obtain coverage.

### 4. Define and Perform Manual Exploration

Create `manual-test-cases.md`. Keep manual work separate from automated work.
Include scenarios requiring human judgment, such as visual composition,
accessibility, timing windows, unusual input, external handoffs, and user
journeys not faithfully reproducible in the available automation.

Record actual observations only after they occur. Mark not-run, blocked, and
failed scenarios plainly.

### Report Traceability

Create `report.md` from the completed artifacts. Map each requirement or DoD
item to automated evidence, manual evidence, and its factual status. State
remaining risk and blockers. Do not call the task complete unless every
required item is evidenced or an explicit owner accepts the limitation.

## Quality Gates

Before finalizing, verify that:

- every requirement has a traceable treatment or an explicit blocker;
- each automated check has a risk-based reason and real result;
- manual checks cover the gaps that automation cannot prove;
- evidence sources are specific enough for another person to inspect;
- findings distinguish fact, inference, and open question;
- the artifact chain contains no credentials, private endpoints, personal data,
  internal identifiers, or copied proprietary content.

Use `references/artifact-contract.md` for mandatory artifact sections and
`assets/project-agent-rules.md` when a project needs a concise local rule. Read
`references/eleven-principles.md` before finalizing complex work.

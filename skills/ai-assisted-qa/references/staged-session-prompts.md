# Controlled QA Session Templates

These are five separate Codex messages, not one long request. Send the next
message only after reviewing the artifact from the preceding one. Replace every
`<...>` value with a real local value. Do not put private URLs, credentials,
customer data, or production identifiers in a prompt that will be shared.

The artifact root is deliberately configurable. A project may use
`qa/<task-id>/`, `test_cases/<task-id>/`, or another local-only directory.

## 1. Analysis

```text
Use the local AGENTS.md and the ai-assisted-qa SKILL.md while working on task
<task-id>. Perform point 1 only: full QA analysis. Do not start the algorithm,
automated checks, a manual test case, or a report.

Artifact location: <case-root>/<task-id>/analysis.md. First confirm that the
task directory exists; create only that directory if it is missing.

Use the local code and confirmed delivery material as sources of truth. Before
making any conclusion, collect and reconcile all available information:
1. Task description, acceptance criteria, DoD, status, and custom fields.
2. Every task note, attachment, screenshot, linked task, parent item, and
   relevant sibling item.
3. All related pull requests, merged revisions, and delivery notes.
4. The actual implementation and existing tests in the local repository.
5. The route atlas, similar approved task artifacts, and known process
   barriers, if the project maintains them.

The complete analysis must contain, at minimum:
1. What was checked in the task tracker and which source is authoritative.
2. Delivery status: whether the expected code is present, absent, or only
   partially present.
3. Concrete implementation facts with file/module references.
4. How the behavior worked before the change.
5. What changed and which user or business problem it addresses.
6. A requirement/DoD matrix with a proposed proof for every item.
7. The full changed surface: UI, API, data, asynchronous jobs, integrations,
   permissions, state transitions, and dependent pages or consumers when they
   apply.
8. Risks and regression zones, with a factual reason for every risk.
9. Constraints, missing evidence, assumptions, and blockers.
10. For a UI task: whether browser automation is possible and necessary now,
    what it can prove, and what must remain a manual check.

Show the complete analysis in chat without shortening it. Save exactly that
reviewed text to analysis.md when this project permits saving at the analysis
stage. Do not silently rewrite, compress, or restructure the artifact after it
has been reviewed.
```

## 2. Verification Algorithm

```text
Use the local AGENTS.md and the ai-assisted-qa SKILL.md while working on task
<task-id>. Perform point 2 only: a verification algorithm. Use the approved
analysis at <case-root>/<task-id>/analysis.md as a source of truth. Do not
write a manual test case or report and do not begin unrelated execution.

Before new route discovery, read the project route atlas and similar confirmed
algorithms. Check known process barriers separately. Reuse a proven route when
it fits; do not rediscover it from scratch.

First decide which contours and entry points are actually needed, where
applicable:
- local repository and repository-native tests;
- task tracker and delivery revision;
- API or service endpoint;
- browser route and browser automation;
- data store, queue, job runner, object storage, search index, or integration;
- access prerequisites such as a read-only VPN or approved credentials.

Perform a read-only preflight of the required entry points. If an
infrastructure or process blocker prevents a required proof, record it early
with its scope impact and stop the affected branch instead of inventing a
result.

Write a reproducible algorithm, not generic testing advice. It must include:
1. Case signature and the DoD/risk scope it covers.
2. Preconditions, target contours, and confirmed entry points.
3. Route-memory decision: reused route, task-specific additions, and the
   intended compare -> reuse/update/add decision.
4. A minimal ordered route, normally three to six core steps, with explicit
   branches where the task requires them.
5. For every step: user action, agent action, system/layer, observable proof,
   expected factual outcome, and stop condition or handoff.
6. The automation/manual boundary and the exact evidence each part must leave.
7. What must be changed or escalated if a step reveals a problem.
8. A short factual end-state that would allow the next stage to proceed.

Show the complete algorithm in chat first. Save the same reviewed text to
<case-root>/<task-id>/algorithm.md when the project allows saving at this
stage. After the route is established, synchronize route memory only through
compare -> reuse/update/add and only with confirmed reusable knowledge. Do not
start automated checks, the manual test case, or the report in this turn.
```

## 3. Automated Checks and Evidence

```text
Use the local AGENTS.md and the ai-assisted-qa SKILL.md while working on task
<task-id>. Perform point 3 only: automated checks and their evidence. Use the
approved analysis and algorithm from <case-root>/<task-id>/ as sources of
truth. Do not write a manual test case or the final report.

Choose the smallest test layer that can prove each changed risk. Prefer the
repository-native runner when it exists. Before writing a new test, choose its
format deliberately:
- a short linear shell smoke check only for a small, simple flow;
- Python or the repository-native runner for parsing, branching, retries,
  data selection, contract comparison, or evidence collection;
- browser automation only for browser-visible UI, navigation, DOM, or network
  behavior.

Before the first useful action, preflight only the dependencies actually used.
Run only authorized, non-destructive checks. An executable test must be run
end-to-end and be repeatable before it is presented as a reusable artifact or
CI candidate.

For each automated scenario, record:
1. Scenario ID and the exact requirement/risk it proves.
2. Test layer and why that layer is sufficient.
3. Preconditions, selected data/state, and target contour.
4. The repository-native command or reproducible procedure.
5. Observable assertions and the expected result.
6. Actual factual result, status, and exact evidence location.
7. A limitation or blocker, when present.

For a browser-visible change, preserve human-readable evidence of the changed
behavior: a video for an action or transition, or a focused screenshot for a
static visual result. Raw logs, JSON, traces, and network responses may support
the proof but do not replace it. A failed scenario and its available evidence
must remain visible; never omit it to make a run look green.

Save only the artifacts that were actually created: an executable test or test
bundle when requested for rerun/CI, a separate automated-check report, and an
evidence archive when multiple factual files exist. Do not create a manual test
case or a final report in this stage.
```

## 4. Manual Test Case

```text
Use the local AGENTS.md and the ai-assisted-qa SKILL.md while working on task
<task-id>. Perform point 4 only: prepare the manual test case. Use the approved
analysis, algorithm, and automated-check evidence under <case-root>/<task-id>/
as sources of truth. Do not invent execution results and do not write the final
report.

Before drafting, confirm that the available facts are sufficient to cover the
complete DoD. If they are not, list the exact missing facts and stop instead of
guessing.

Prepare one complete manual test case with this fixed structure:
1. Task title and identifier.
2. Description.
3. Analysis for the test case: only previous behavior, changed behavior,
   problem solved, and affected regression zones.
4. Preconditions: only what a tester needs, including an explicit real entry
   point for every external contour used by the steps.
5. Steps: independently numbered, one concrete tester action per step, with
   one observable expected result directly below it.

The test case must cover the full DoD and every user-visible state that remains
outside automated proof. It must not copy an automated matrix merely because
automation ran. For UI work, include the relevant visual/design comparison and
the states where the changed block must not appear. For API or technical steps,
include only confirmed, reproducible data and procedures; never replace missing
runtime values with placeholders or guesses. Expected results describe
observable behavior, not source-code names or internal constants.

Show the complete test case in chat. Do not save, reword, normalize URLs, or
reorder steps until the reviewer approves the exact text. After approval, save
the approved text 1:1 as <case-root>/<task-id>/manual-test-cases.md.
```

## 5. Final QA Report

```text
Use the local AGENTS.md and the ai-assisted-qa SKILL.md while working on task
<task-id>. Perform point 5 only: write the final QA report. Use the approved
manual test case and the factual automated and manual execution evidence under
<case-root>/<task-id>/ as sources of truth. Do not publish the report anywhere
unless publication is explicitly requested after the exact text is approved.

The report is a factual record, not a summary invented from the plan. Preserve
the manual test-case steps in the same order and at the same level of detail.
For every executed step show the action, expected result, and actual result.
Do not collapse several approved test-case steps into one report item. Keep the
original DoD wording; report a limitation beside it instead of silently
narrowing it.

Use the full report structure from references/final-report-template.md. List
every current relevant artifact: analysis, algorithm, automated test/report,
evidence package, manual test case, and manual media where applicable. Agent
actions must prove product behavior, regressions, scope boundaries, or blockers;
document-format checks are internal preflight and do not belong in the report.

Before saving or publishing, mechanically verify that the report reproduces
the approved manual test-case actions, expected results, and literal technical
fragments where applicable. If any requirement lacks evidence, mark it blocked
or not run. Save only the approved report text without mutation.
```
